# LSFD202201V3

The 3rd version of [LSFD202201 Class Website](https://ls202201.pythonanywhere.com)  
[中文](./README_zh.md)
[English](./README.md)
## Aim

The aim of this website is to contribute to our class in our own way and to challenge our programming skills.

## About our class
LSFD 202201, located in YP District, SH, China. We are a formal school class in Lansheng Fudan Middle school.  
Address: 8 Shijie Rd.(near Nenjiang Rd.)  
Transportation: Shanghai Metro Line 8, Shanghai Metro Line 10, 90, 966, 55, 大桥三线
## Contributors

[Andy Zhou](https://github.com/z-t-y "ZTY")  
[Rice Zong](https://github.com/rice0208 "ZYT")

*(whisper*  
[Rice Zong](https://github.com/rice0208 "ZYT")
actually did nothing for THIS VERSION
but finishing the 2nd version of the website. [doge]

## Special Thanks To

#### Projects
- [Flask](https://github.com/pallets/flask)
- [Bootstrap](https://github.com/twbs/bootstrap)
- [Bootstrap-Flask](https://github.com/greyli/bootstrap-flask)
- [Flask-WTF](https://github.com/lepture/flask-wtf)
- [Flask-Share](https://github.com/greyli/flask-share)
- [MyQR](https://pypi.org/project/MyQR/)
#### Books
- [Flask Web Development](https://helloflask.com)
#### People
- [GreyLi](https://greyli.com)

Without these projects, the website cannot be developed.  
At the same time, thanks to [GreyLi](https://greyli.com), it was his <i>Flask Web Development</i>
that took me into the wonderful world of Flask.

## How to run the website on your local machine
1. Fork and Clone the project from Github or Gitee and name the folder as you like
2. Create a virtual environment and run
```bash
pip3 install -r requirements.txt
```
3. Create .env file, take a look at my config.py and set the passwords as you like.  
   Also, you should create a data.sqlite file in project root.
4. Open flask shell and run  
```python
>>> from . import db
>>> db.create_all()
```
5. Run `flask run` in project root.
6. Go to localhost:5000/articles, you will be redirected to the upload page.
7. Fill out the form.
8. All done! You can change the project as whatever you want it to be!  
(Remember to make it open-source because this is a GPL3 licensed project.)


## Release Notes
### V3.6.0 7/24/2020
1. Refactor Project
2. Change navbar theme

### V3.5.2 7/23/2020
1. Change default index theme to light
2. Add better pagination support
3. Refactor the project

### V3.4.0 7/20/2020
1. Give administrators the power to edit articles
2. Refactor the project with [Bootstrap-Flask](https://github.com/greyli/bootstrap-flask) and [Bootstrap4](https://github.com/twbs/bootstrap)
3. Add fade-in effect on index page
4. Add a datepicker on upload page

### P.S.
I'm going to stop developing this website for some months
because I'll have to learn more advanced Flask skills to
keep on developing. I'll let Rice Zong manage this website.