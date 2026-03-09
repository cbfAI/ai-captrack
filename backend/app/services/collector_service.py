from typing import Dict, Any
from datetime import datetime

from app.scrapers.huggingface_scraper import HuggingFaceScraper
from app.scrapers.github_scraper import GitHubScraper
from app.scrapers.futuretools_scraper import FutureToolsScraper
from app.scrapers.openrouter_scraper import OpenRouterScraper
from app.services.deduplication_service import deduplicate_capabilities


# 全局采集进度
collection_progress = {
    "status": "idle",  # idle, running, completed, error
    "current_source": None,
    "progress": 0,  # 0-100
    "total_sources": 3,  # HuggingFace + GitHub + OpenRouter
    "current_source_index": 0,
    "results": [],
    "start_time": None,
    "end_time": None,
}

def trigger_collection(db) -> Dict[str, Any]:
    global collection_progress
    
    # 重置进度
    collection_progress.update({
        "status": "running",
        "current_source": None,
        "progress": 0,
        "current_source_index": 0,
        "results": [],
        "start_time": datetime.now().isoformat(),
        "end_time": None,
    })

    scrapers = [
        HuggingFaceScraper(),
        GitHubScraper(),
        OpenRouterScraper(),
        # FutureToolsScraper(),
        # MockScraper(),
    ]

    total_collected = 0
    results = []

    for i, scraper in enumerate(scrapers):
        collection_progress.update({
            "current_source": scraper.source.value,
            "current_source_index": i + 1,
            "progress": int((i / len(scrapers)) * 100),
        })
        
        try:
            capabilities = scraper.collect()
            
            # 打印前3条数据的详细信息用于调试
            print(f"\n=== 采集到 {len(capabilities)} 条数据 ===")
            for j, cap in enumerate(capabilities[:3]):
                print(f"\n--- 第 {j+1} 条 ---")
                print(f"名称: {cap.name}")
                print(f"描述: {cap.description}")
                print(f"类型: {cap.capability_type}")
                print(f"Stars: {cap.stars}")
                print(f"Key Features: {cap.key_features}")
            
            deduplicated = deduplicate_capabilities(db, capabilities, scraper.source)
            total_collected += len(deduplicated)
            result = {
                "source": scraper.source.value,
                "collected": len(capabilities),
                "after_dedup": len(deduplicated),
                "status": "success",
            }
            results.append(result)
            collection_progress["results"].append(result)
        except Exception as e:
            print(f"\n采集失败: {e}")
            import traceback
            traceback.print_exc()
            result = {
                "source": scraper.source.value,
                "collected": 0,
                "after_dedup": 0,
                "status": "error",
                "error": str(e),
            }
            results.append(result)
            collection_progress["results"].append(result)

    collection_progress.update({
        "status": "completed",
        "progress": 100,
        "end_time": datetime.now().isoformat(),
    })

    return {
        "total_collected": total_collected,
        "results": results,
    }

def get_collection_progress() -> Dict[str, Any]:
    """获取采集进度"""
    global collection_progress
    return collection_progress