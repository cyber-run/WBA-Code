import logging
from pathlib import Path
import cv2
import time
from src.experiment_manager import ExperimentManager
from src.config import CONFIG

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main entry point for the real-time wingbeat analyzer and optic flow experiment"""
    try:
        # Use test video from root directory
        root_dir = Path(__file__).parent
        video_path = root_dir / "test_video.avi"
        output_dir = root_dir / "output"
        
        # Ensure video exists
        if not video_path.exists():
            raise FileNotFoundError(f"Test video not found: {video_path}")
        
        # Setup display window for optic flow
        cv2.namedWindow("Optic Flow", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Optic Flow", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        
        # Define experiment parameters
        frame_size = (800, 800)  # Adjust as needed for your display
        experiment_name = "realtime_test"
        
        # Define gain cycle: (duration in seconds, gain)
        gain_cycle = [
            (10, 25),   # High gain for 10s
            (10, 0),    # No stimulus for 10s
            (10, 12.5), # Medium gain for 10s
            (10, 0)     # No stimulus for 10s
        ]
        
        logger.info("Initializing experiment...")
        experiment = ExperimentManager(
            frame_size=frame_size,
            video_path=video_path,  # Pass video path
            min_amplitude=30,
            max_amplitude=120
        )
        
        # Countdown before starting
        logger.info("Starting experiment in:")
        for i in range(3, 0, -1):
            logger.info(f"{i}...")
            time.sleep(1)
            
        logger.info("Running experiment...")
        # Run experiment and collect data
        data = experiment.run_experiment(experiment_name, gain_cycle)
        
        # Save data
        output_dir = Path(__file__).parent / "output"
        output_dir.mkdir(exist_ok=True)
        
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        output_file = output_dir / f"experiment_data_{timestamp}.csv"
        
        import pandas as pd
        df = pd.DataFrame(data, columns=['Time', 'Wingbeat Amplitude', 'Speed'])
        df.to_csv(output_file, index=False)
        
        logger.info(f"Data saved to: {output_file}")
        logger.info("Experiment completed successfully")
        return 0
        
    except KeyboardInterrupt:
        logger.info("Experiment interrupted by user")
        return 1
    except Exception as e:
        logger.error(f"Experiment failed: {str(e)}")
        return 1
    finally:
        cv2.destroyAllWindows()

if __name__ == "__main__":
    exit(main()) 