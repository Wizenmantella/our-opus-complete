#!/usr/bin/env python3
"""
Custom Test - Let's create something incredible!
"""

import asyncio
from working_demo import WorkingVideoCreator

async def create_custom_content():
    creator = WorkingVideoCreator()
    
    # Your custom prompts - let's make something incredible!
    custom_prompts = [
        {
            "prompt": "The hidden physics of how glass breaks in slow motion",
            "duration": 45,
            "style": "world_model"
        },
        {
            "prompt": "Why TikTok's algorithm is secretly training your brain",
            "duration": 60,
            "style": "cultural_innovation"
        },
        {
            "prompt": "I spent 30 days creating content with AI and this happened",
            "duration": 90,
            "style": "viral_documentary"
        }
    ]
    
    print("🚀 Creating incredible custom content!")
    print("="*60)
    
    results = []
    for prompt_data in custom_prompts:
        print(f"\n🎯 Creating: {prompt_data['prompt']}")
        
        result = await creator.create_video(
            prompt=prompt_data["prompt"],
            duration=prompt_data["duration"]
        )
        
        results.append(result)
        
        print(f"✅ Created Project {result.project.project_id}")
        print(f"   Viral Score: {result.metadata['viral_score']:.1%}")
        print(f"   Innovation: {result.metadata['aesthetic']['innovation_level']:.1%}")
        print(f"   Style: {result.metadata['aesthetic']['name']}")
    
    print(f"\n🎉 Created {len(results)} incredible videos!")
    print("🌐 Check the HTML previews to see the magic!")
    
    return results

if __name__ == "__main__":
    asyncio.run(create_custom_content())