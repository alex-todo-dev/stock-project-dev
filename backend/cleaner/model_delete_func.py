import os
from env import env
from logger import logger

def delete_model_files(strings_to_delete):
    """
    Delete model files that start with any of the specified strings.

    Parameters
    ----------
    strings_to_delete : list of str
        A list of strings; files starting with any of these strings will be deleted.

    Returns
    -------
    dict
        A dictionary containing the status of the operation.
    """
    # Log the files that are scheduled for deletion
    print("Files to be deleted:", strings_to_delete)
    logger.info(f"MODEL TRAINNER:Files to be deleted: {strings_to_delete}")
    # Retrieve the folder path where the model files are stored
    folder_path = env.model_path
    lstm_folder_path = env.lstm_model_path

    # Iterate through the files in the specified folder
    for filename in os.listdir(folder_path):
        # If the filename starts with any of the specified strings, delete the file
        if any(filename.startswith(s) for s in strings_to_delete):
            os.remove(os.path.join(folder_path, filename))
            logger.info(f"MODEL Cleaner:Deleted file: {filename}")
    
    # Itereta trough the files and delete lstm 
    for filename in os.listdir(lstm_folder_path):
        # If the filename starts with any of the specified strings, delete the file
        if any(filename.startswith(s) for s in strings_to_delete):
            os.remove(os.path.join(folder_path, filename))
            logger.info(f"MODEL Cleaner:LSTM Deleted file: {filename}")


    # Return the status of the operation
    return {"status": "models deleted"}
