# ProjectCreator Application using `ttkbootstrap`

ProjectCreator is a GUI application written in Python that simplifies the creation of new projects with local and remote git repositories, virtual environments, `.gitignore`, and `requirements.txt` files. The application is built using `ttkbootstrap` for interface styling.

![Screenshot](images/screenshot.png)

## Table of Contents

- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Features](#features)
- [Files](#files)
- [Contribution](#contribution)
- [License](#license)

## Installation

To run the application, you need to clone this repository to your local disk:

```sh
git clone https://github.com/your-username/project-creator.git
cd project-creator
```

You need Python and the TtkBootstrap library installed. You can install them using the following commands:

```sh
pip install ttkbootstrap
```


You can also use the requirements.txt file:

```sh
pip install -r requirements.txt
```

## Running the Application

To run the application, simply execute the following command in the terminal while in the project directory:

```sh
python project_creator.py
```

## Features

- Create new project folders with virtual environments
- Initialize git repositories and link to remote repositories
- Automatically create `.gitignore` and `requirements.txt` files
- Perform initial commit and push to remote repository
- User-friendly interface styled with `ttkbootstrap`

## Files

### Main Application Files

- **project_creator.py**: Contains the main application code, initializes the main window, creates the widgets, and handles the layout.

### Dependencies

- **ttkbootstrap**: Library for styling Tkinter applications.

## Contribution

If you want to contribute to the development of this project, open an issue or create a pull request. New features, bug fixes, and code optimizations are always welcome.

## License

The project is available under the MIT license. Details can be found in the LICENSE file.