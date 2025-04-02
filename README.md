# Project Documentation

## Overview
This repository contains a Bash script that demonstrates the usage of regular expressions and common Linux commands for text processing and system information retrieval.

## Script Functionality
The `regex.sh` script performs the following tasks:

1. **Identify all grammatical forms of a surname**  
   - Regular expression: `Супрун(а|у|ом|і|е)`

2. **Identify all grammatical forms of a given name**  
   - Regular expression: `Павл(о|а|у|ом|і|е)`

3. **Match phone codes of major cities in a specific region**  
   - Regular expression: `0432[-\s]?\d{3}[-\s]?\d{2}[-\s]?\d{2}`

4. **Display a list of all system users with Bash as their default shell**  
   - Command: `cat /etc/passwd | grep bash`

5. **Show all lines from `/etc/group` that start with "daemon"**  
   - Command: `grep "^daemon" /etc/group`

6. **Show all lines from `/etc/group` that do not contain "daemon"**  
   - Command: `grep -v "daemon" /etc/group`

7. **Count the number of README files in the `/etc` directory, excluding files matching `README.a_string`**  
   - Command: `find /etc -type f -name 'README' -not -name 'README.*' | wc -l`

8. **List all files in the home directory that were modified in the last 10 hours**  
   - Command: `find ~/ -type f -mmin -600`

## Usage
To run the script, execute the following command in the terminal:
```bash
bash regex.sh
```
Ensure that the script has execution permissions:
```bash
chmod +x regex.sh
./regex.sh
```

## Requirements
- Linux-based operating system
- Bash shell
- Utilities: `grep`, `awk`, `sed`, `find`

## Contribution
Contributions are welcome. If you find any issues or have suggestions for improvements, feel free to create a pull request.

## License
This project is licensed under the MIT License.
