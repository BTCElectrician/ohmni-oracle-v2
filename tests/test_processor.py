import asyncio
from pathlib import Path
from utils.drawing_processor import DrawingProcessor

async def test_processing():
    processor = DrawingProcessor()
    
    # Test single file
    test_pdf = Path("path/to/test.pdf")
    result = await processor.process_drawing(test_pdf)
    print(f"Tables found: {len(result['tables'])}")
    print(f"Text blocks found: {len(result['text_blocks'])}")
    
    # Test batch processing
    files = [Path("file1.pdf"), Path("file2.pdf")]
    results = await processor.process_batch(files)
    for file, result in results.items():
        if "error" in result:
            print(f"Error processing {file}: {result['error']}")
        else:
            print(f"Processed {file}:")
            print(f"- Tables found: {len(result.get('tables', []))}")
            print(f"- Text blocks found: {len(result.get('text_blocks', []))}")
            if result.get('metadata'):
                print(f"- Pages: {result['metadata'].get('page_count')}")
                print(f"- Languages detected: {result['metadata'].get('languages', ['unknown'])}")

async def run_tests():
    """Run a complete test suite"""
    # Test valid file
    await test_processing()
    
    # Test non-existent file
    try:
        processor = DrawingProcessor()
        await processor.process_drawing(Path("nonexistent.pdf"))
    except FileNotFoundError as e:
        print(f"Successfully caught file not found: {e}")
    
    # Test batch processing with mixed valid/invalid files
    mixed_files = [
        Path("valid.pdf"),
        Path("nonexistent.pdf"),
        Path("another_valid.pdf")
    ]
    processor = DrawingProcessor()
    results = await processor.process_batch(mixed_files)
    print("\nBatch processing results:")
    for file, result in results.items():
        print(f"{file}: {'Success' if 'error' not in result else f'Error - {result['error']}'}")

if __name__ == "__main__":
    asyncio.run(run_tests()) 