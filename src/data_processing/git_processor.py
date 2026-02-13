import pandas as pd
from git import Repo
import os
from src.utils.logger import get_logger

logger = get_logger("GitProcessor")

class FlaskEvolutionMiner:
    def __init__(self, repo_path):
        self.repo_path = repo_path
        self.repo = Repo(repo_path)

    def extract_commit_history(self, output_csv, limit=500, since=None, until=None):
        """
        :param limit: 最大提取数量
        :param since: 开始日期 (YYYY-MM-DD)
        :param until: 结束日期 (YYYY-MM-DD)
        """
        logger.info(f"Git分析启动: 范围={since} 至 {until}, 限制数量={limit}")
        
        # 构建 Git 过滤参数
        kwargs = {"max_count": limit}
        if since: kwargs["since"] = since
        if until: kwargs["until"] = until

        commits = list(self.repo.iter_commits('main', **kwargs))
        
        if not commits:
            logger.warning("在指定范围内未找到任何提交！")
            return pd.DataFrame()

        data = []
        for c in commits:
            msg = c.message.lower()
            category = "feature" if "feat" in msg else "bugfix" if "fix" in msg else "docs" if "doc" in msg else "refactor"
            
            data.append({
                "hash": c.hexsha,
                "author": c.author.name,
                "date": c.authored_datetime,
                "category": category,
                "summary": c.summary[:60]
            })
            
        df = pd.DataFrame(data)
        df.to_csv(output_csv, index=False, encoding="utf-8-sig")
        logger.info(f"成功提取 {len(df)} 条提交记录至 {output_csv}")
        return df