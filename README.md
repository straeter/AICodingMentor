# security_code_scan
Use LLMs to scan your code for security issue.

The script goes through the files of your repo, scans them one by one and outputs the security issues found in a json file.

## Installation
1. Install the required packages
```bash
pip install -r requirements.txt
```
(optionally you can first create a virtual environment)

2. Create a .env file in the root folder with the following content (or copy/paste the content of the .env.example file)
```bash
OPENAI_API_KEY=<your_openai_api_key>
```

3. If you want to connect to your Github account, you also have to add these environment variables:
```bash
GITHUB_USERNAME=<your_github_username>
GITHUB_PAT=<your_github_personal_access_token>
```
You can create your personal access token on Github by going to Settings -> Developer settings -> Personal access tokens -> Generate new token.
Make sure to give the token the right permissions to read repositories and metadata.

## Usage

### Flask app
1. Run the following command to start the flask app
```bash
python main.py
```
2. Go to http://127.0.0.1:5000/ in your browser
3. Either select a local directory or one of your github repositories, choose branch and files and start the scan.
4. The results tab shows the result of the scan (can take a few minutes depending on the size of your scan).

### Terminal usage
1. Run the following command to scan your code in your folder
```bash
python scan.py <path_to_folder> --out-file <output_file> --file-types <file_types>
```
- path_to_folder: the path to the folder you want to scan
- output_file: the path to the output file (otherwise will default to the current date)
- file_types: the file types you want to scan (default to .py)

The output will be saved in folder security_scans.

2. Run the following command to go through the issues one by one:
```bash
python eval.py <path_to_output_file> --level <level>
```
- path_to_output_file: the path to the output file with security scan results
- level: the level (1-5) of the issues you want to go through (default to None which means all levels)

## Format of the output file

The output file of the security scan is a json file with the following format:
```json
{
    "filepath": [
        {
            "title": "title of the issue",
            "reference": "problematic lines (with numbers)",
            "reason": "explanation of the issue",
            "level": "level of security issue: 1 (low) - 5 (high)"
        }
    ]
}
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

