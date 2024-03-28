from src import create_app
import os

yaml_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
app = create_app(yaml_path)

if __name__ == '__main__':
	app.run('0.0.0.0', port=5001)
