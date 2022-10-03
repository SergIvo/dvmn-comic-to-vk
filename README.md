# Posting comics to VKontakte group

## About

This application downloads  random comics from [xkcd.com](https://xkcd.com) and publishes it into VKontakte group. Group is set by exporting it's ID as environment variable.

This application created for educational purposes as part of an online course for web developers at [dvmn.org](https://dvmn.org/)

## Running the application

1. Download application from GitHub by using `git clone` command:
```
git clone https://github.com/SergIvo/dvmn-comic-to-vk
```
2. Create virtual environment with python [venv](https://docs.python.org/3/library/venv.html) library to avoid conflicts with other versions of the same packages:
```
python -m venv venv
```
Use `pip` package manager to install dependencies from "requirements.txt" in created virtual environment:
```
pip install -r requirements.txt
```
To make application, you have to set two environment variables:
```
export VK_APP_ID="ID of your VK application"
export VK_IMPLICIT_FLOW_TOKEN="your VK API authentication token"
export VK_GROUP_ID="ID of the group you want to post to"
```
If you don't have VKontakte application, you can create it [here](https://vk.com/editapp?act=create). To make application work properly, choose `Standalone` option when creating it.
If you run this script without authentication, it will print the link to authentication page to console. Follow the link, make necessary permissions and copy token from page URL.

If you don't want to set environment variables manually, you can create [.env](https://pypi.org/project/python-dotenv/#getting-started) file and store all variables in it. 

Run `main.py` to make application download random comic and post it to your group:
```
python main.py
```
After finishing the process, application will print following message to console:
```
Комикс опубликован в группе.
```