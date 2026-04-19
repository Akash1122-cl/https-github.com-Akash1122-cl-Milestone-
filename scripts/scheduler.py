import os
import sys
import subprocess
import logging
from datetime import datetime

def setup_logging():
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    # Force sys.stdout to handle utf-8 to prevent UnicodeEncodeError during printing of emojis
    sys.stdout.reconfigure(encoding='utf-8')
    
    log_file = os.path.join(log_dir, "scheduler.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger("Scheduler")

def run_script(script_path, logger):
    logger.info(f"Starting execution of {script_path}")
    try:
        # Run process and capture output
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        process = subprocess.Popen(
            [sys.executable, "-u", script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            bufsize=1,
            universal_newlines=True,
            env=env
        )
        
        # Log output in real-time
        for line in process.stdout:
            logger.info(f"[{os.path.basename(script_path)}] {line.strip()}")
            
        process.wait()
        
        if process.returncode != 0:
            logger.error(f"Execution of {script_path} failed with return code {process.returncode}")
            return False
            
        logger.info(f"Successfully completed execution of {script_path}")
        return True
    except Exception as e:
        logger.error(f"Error running {script_path}: {str(e)}")
        return False

def main():
    logger = setup_logging()
    logger.info("Starting local pipeline scheduler")
    
    scripts_to_run = [
        "scripts/ingest.py",
        "scripts/index.py"
    ]
    
    # Check if we are in the correct directory
    if not os.path.exists("scripts/ingest.py"):
        logger.error("Please run this script from the root of the project (e.g. python scripts/scheduler.py)")
        sys.exit(1)
    
    for script in scripts_to_run:
        success = run_script(script, logger)
        if not success:
            logger.error("Pipeline failed. Aborting subsequent steps.")
            sys.exit(1)
            
    logger.info("Local pipeline scheduler completed successfully")

if __name__ == "__main__":
    main()
