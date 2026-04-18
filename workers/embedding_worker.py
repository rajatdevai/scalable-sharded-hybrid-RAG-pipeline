import time
import logging
from workers.queue import pop_from_queue, get_queue_size
from app.services.ingestion_services import ingest_documents

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_worker():
    logging.info("Starting Embedding Worker...")
    
    while True:
        try:
            # 1. Pop from queue
            data = pop_from_queue()
            
            if data:
                text = data.get("text")
                logging.info(f"Processing document (Queue size: {get_queue_size()})")
                
                # 2. Process (Chunk -> Embed -> Store)
                # We reuse the ingest_documents logic
                ingest_documents([text])
                
                logging.info("Successfully ingested document.")
            else:
                # No data, wait for a bit
                time.sleep(2)
                
        except Exception as e:
            logging.error(f"Error in worker loop: {str(e)}")
            time.sleep(5)

if __name__ == "__main__":
    run_worker()
