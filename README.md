# timeChecker

## Table of Contents
1. [Description](#description)
2. [Installation](#installation)
3. [Usage](#usage)
5. [ToDo](#todo)
6. [Contributing](#contributing)
7. [License](#license)
8. [Author](#author)

## Description
This is a simple application that keeps the time you're in an application. It's made to see if you spend too much time on an application so you can reduce the time on it. The project does need some work, because as of now it uses the title of the application, but most applications don't use their own name in the title, rather they use what you're doing, example: visual studio code displays the current project you're working in.

## Installation
### Currently only supporting windows!!!
1. Clone this github repository
2. Open the project in visual studio code (or any other IDE)
3. Compile the project with:
```bash
pyinstaller --onefile --noconsole --icon=favicon.ico --add-data "favicon.ico;." timeChecker.py
```
4. copy and paste the favicon.ico file into the `dist/` folder.
5. Run the executable in the `dist/` folder.
6. (OPTIONAL) Create a shortcut to the executable and move that shortcut into the `programs` (press `WIN+R` and type `shell:programs`) folder to run the application on startup.
7. Done!

## Usage
1. Run the application
2. Press the `Start Tracking` button
3. The application will now track the time you're in an application and it'll show you the time you've spent in the application in a pie chart.
4. Press the `Stop Tracking` button to stop tracking the time.
5. Press the `Save Tracked Data` button to save the pie chart as a png file, and the data as a excel file. (This will also clear the pie chart data afterwards!)
6. Done!

## ToDo
- [ ] Add support for linux
- [ ] Add support for mac
- [ ] Make sure the main application name is used not the application's title 

## Contributing
If you want to contribute to this project, feel free to fork this project and make a pull request. I'll review the pull request and merge it if it's a good addition to the project.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author
- [HowlingArcher](https://github.com/HowlingArcher)