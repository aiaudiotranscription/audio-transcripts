import send_email
import whisper_access
import download_attachments
import os


INPUT_DIRECTORY = os.path.split(os.getcwd())[0] + "\\audio_files\\"
OUTPUT_DIRECTORY = os.path.split(os.getcwd())[0] + "\\transcripts\\"


def main():
    files_and_senders = download_attachments.download_attachments(INPUT_DIRECTORY)
    pipe = whisper_access.load_model()
    server = send_email.get_server()
    for file_name, sender in files_and_senders:
        input_file = INPUT_DIRECTORY + file_name
        output_file = OUTPUT_DIRECTORY + input_file.split("\\")[-1] + ".txt"
        whisper_access.transcribe_file(input_file, output_file, pipe=pipe)
        if sender:
            send_email.send_attachment_to_address(output_file, sender, file_name, server=server)


if __name__ == '__main__':
    main()
