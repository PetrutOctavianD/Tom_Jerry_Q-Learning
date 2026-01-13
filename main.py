import argparse
import sys
from q_learning import QLearningTrainer
from visualization import MazeVisualizer
from config import Config

def main():
    parser = argparse.ArgumentParser(
        description='Tom & Jerry Q-Learning - Vizualizare algoritm',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
        """
    )
    
    parser.add_argument('episodes', type=int, nargs='?', default=10,
                       help='Numar de episoade de vizualizat')
    
    args = parser.parse_args()

    trainer = QLearningTrainer()
    
    trainer.train(episodes=min(100, args.episodes * 2))
    
    visualizer = MazeVisualizer(trainer.env, trainer.agent)
    visualizer.run_training_visualization(num_episodes=args.episodes)

if __name__ == "__main__":
    main()