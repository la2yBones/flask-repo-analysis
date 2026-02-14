import pandas as pd
from git import Repo
import os
from src.utils.logger import get_logger

logger = get_logger("GitProcessor")

class FlaskEvolutionMiner:
    def __init__(self, repo_path):
        self.repo_path = repo_path
        if not os.path.exists(repo_path):
            logger.error(f"路径不存在: {repo_path}")
            raise FileNotFoundError(f"找不到 Git 仓库: {repo_path}")
        self.repo = Repo(repo_path)
    def classify_message(self, message):
        """
        根据提交信息摘要对任务进行分类
        """
        msg = message.lower()
        if any(keyword in msg for keyword in ['fix', 'bug', 'close', 'issue']):
            return "bugfix"
        if any(keyword in msg for keyword in ['feat', 'add', 'new', 'support']):
            return "feature"
        if any(keyword in msg for keyword in ['doc', 'readme', 'tutorial']):
            return "docs"
        if any(keyword in msg for keyword in ['refactor', 'cleanup', 'style']):
            return "refactor"
        return "others"
    def extract_commit_history(self, output_csv, limit=500, since=None, until=None):
        """
        :param limit: 最大提取数量
        :param since: 开始日期 (YYYY-MM-DD)
        :param until: 结束日期 (YYYY-MM-DD)
        """
        logger.info(f"Git分析启动: 范围={since} 至 {until}, 限制数量={limit}")
        
        # 构建 Git 命令参数
        kwargs = {"max_count": limit}
        if since: kwargs["since"] = since
        if until: kwargs["until"] = until

        # 获取 Commit 列表
        try:
            commits = list(self.repo.iter_commits('main', **kwargs))
        except Exception:
            # 兼容一些仓库主分支名为 master 的情况
            commits = list(self.repo.iter_commits('master', **kwargs))

        data = []
        for c in commits:
            # 核心提速点：只提取基础属性，绝不访问 c.stats
            summary = c.summary
            data.append({
                "hash": c.hexsha,
                "author": c.author.name,
                "date": c.authored_datetime,
                "category": self.classify_message(summary),
                "summary": summary
            })

        # 转换为 DataFrame 并保存
        df = pd.DataFrame(data)
        
        # 如果数据为空的容错处理
        if df.empty:
            logger.warning("未找到匹配的提交记录。")
            return df

        # 增加 weekday 用于后续报告分析
        df['date'] = pd.to_datetime(df['date'], utc=True)
        df['weekday'] = df['date'].dt.weekday

        # 保存为 CSV (utf-8-sig 兼容 Excel)
        os.makedirs(os.path.dirname(output_csv), exist_ok=True)
        df.to_csv(output_csv, index=False, encoding="utf-8-sig")
        
        logger.info(f"成功提取 {len(df)} 条记录。")
        return df