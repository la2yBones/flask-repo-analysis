import pandas as pd
from git import Repo
import os
from src.utils.logger import get_logger

logger = get_logger("GitProcessor")

class FlaskEvolutionMiner:
    def __init__(self, repo_path):
        self.repo_path = repo_path
        if not os.path.exists(repo_path):
            logger.error(f"Repo path {repo_path} does not exist.")
            raise FileNotFoundError()
        self.repo = Repo(repo_path)

    def extract_commit_history(self, output_csv, max_commits=500):
        """
        优化后的提取逻辑
        :param max_commits: 限制分析的提交数量，防止程序卡死
        """
        logger.info(f"Starting git commit mining (Limited to last {max_commits} commits)...")
        
        # 仅获取最近的指定数量提交
        commits = list(self.repo.iter_commits('main', max_count=max_commits))
        data = []
        
        for i, c in enumerate(commits):
            msg = c.message.lower()
            # 简单的分类逻辑
            if "fix" in msg or "bug" in msg:
                category = "bugfix"
            elif "feat" in msg or "add" in msg:
                category = "feature"
            elif "doc" in msg:
                category = "documentation"
            else:
                category = "refactor/others"
            
            # 关键修改：跳过 c.stats.files 以大幅提升速度
            # 如果你确实需要文件变更数量，可以只针对少量 commit 开启
            data.append({
                "hash": c.hexsha,
                "author": c.author.name,
                "date": c.authored_datetime,
                "category": category,
                "summary": c.summary[:50] # 提取简短摘要
            })
            
            if i % 100 == 0:
                logger.info(f"Processed {i} commits...")

        df = pd.DataFrame(data)
        df.to_csv(output_csv, index=False)
        logger.info(f"History saved to {output_csv}")
        return df