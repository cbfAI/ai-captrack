from typing import Dict, Any, List
from datetime import datetime

from app.scrapers.huggingface_scraper import HuggingFaceScraper
from app.scrapers.github_scraper import GitHubScraper
from app.scrapers.futuretools_scraper import FutureToolsScraper
from app.scrapers.openrouter_scraper import OpenRouterScraper
from app.services.deduplication_service import deduplicate_capabilities, update_capability_llm_fields
from app.services.llm_service import llm_service
from app.models.models import AICapability


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

async def trigger_collection(db, enable_llm_parsing: bool = True) -> Dict[str, Any]:
    """触发数据采集，支持 LLM 智能解析"""
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
    total_llm_parsed = 0
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
            print(f"\n=== Collected {len(capabilities)} items ({scraper.source.value}) ===")
            for j, cap in enumerate(capabilities[:3]):
                # 安全打印，避免 Windows 编码问题
                safe_name = cap.name.encode('ascii', 'ignore').decode('ascii')[:50] if cap.name else 'N/A'
                safe_desc = (cap.description or '')[:100].encode('ascii', 'ignore').decode('ascii')
                print(f"  [{j+1}] {safe_name} | Stars: {cap.stars}")
            
            deduplicated = deduplicate_capabilities(db, capabilities, scraper.source)
            
            # LLM 智能解析
            llm_parsed_count = 0
            if enable_llm_parsing and deduplicated:
                print(f"\n=== 开始 LLM 智能解析 ({len(deduplicated)} 条) ===")
                llm_parsed_count = await _parse_capabilities_with_llm(db, deduplicated)
                print(f"LLM 解析完成: {llm_parsed_count}/{len(deduplicated)}")
            
            total_collected += len(deduplicated)
            total_llm_parsed += llm_parsed_count
            result = {
                "source": scraper.source.value,
                "collected": len(capabilities),
                "after_dedup": len(deduplicated),
                "llm_parsed": llm_parsed_count,
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
                "llm_parsed": 0,
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
        "total_llm_parsed": total_llm_parsed,
        "results": results,
    }


async def _parse_capabilities_with_llm(db, capabilities: List[AICapability]) -> int:
    """使用 LLM 批量解析能力信息"""
    if not capabilities:
        return 0
    
    # 准备待解析数据
    items = [
        {
            "id": cap.id,
            "name": cap.name,
            "description": cap.description or "",
            "metadata_": cap.metadata_ or {},
        }
        for cap in capabilities
    ]
    
    # 批量解析（并发数 3，避免 API 限流）
    parsed_results = await llm_service.batch_parse(items, concurrency=3)
    
    # 更新数据库
    updated_count = 0
    for result in parsed_results:
        cap_id = result.get("id")
        llm_parsed = result.get("llm_parsed")
        
        if cap_id and llm_parsed:
            try:
                update_capability_llm_fields(db, cap_id, llm_parsed)
                updated_count += 1
            except Exception as e:
                print(f"[LLM Update Error] {cap_id}: {e}")
    
    return updated_count

def get_collection_progress() -> Dict[str, Any]:
    """获取采集进度"""
    global collection_progress
    return collection_progress