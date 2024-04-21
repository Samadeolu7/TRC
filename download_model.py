import tensorflow as tf
import tensorflow_hub as hub

def download_and_save_model(module_url, save_path):
    # Load the TF Hub module
    model = hub.load(module_url)

    # Save the model
    tf.saved_model.save(model, save_path)

    print(f"Module {module_url} loaded and saved to {save_path}")

# Specify the module URL and the path where you want to save the model
module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
save_path = '/path/to/save/model'

download_and_save_model(module_url, save_path)