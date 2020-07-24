# LSFD202201V3
兰生复旦中学2022届1班第三版[班级网站](https://ls202201.pythonanywhere.com)  
[中文](./README_zh.md)
[English](./README.md)
## 目标
这个项目旨在以我们自己的方式为班级做贡献以及锻炼我们的编程能力

## 关于我们班
兰生复旦中学，位于上海杨浦区世界路八号。2022届1班（我们班）是其中的一个班级。  
交通方式：轨道交通8号线嫩江路站、轨道交通10号线三门路站、90路公交车、966路公交车、55路公交车、大桥三线

## 项目参与者
[Andy Zhou](https://github.com/z-t-y)  
[Rice Zong](https://github.com/rice0208)  
*(小声bb:*  
*[Rice Zong](https://github.com/rice0208)实际并没有参与这个项目，他只是完成了功能贫乏的第二版\[狗头\]*

## 致谢

#### 开源项目
- [Flask](https://github.com/pallets/flask)
- [Bootstrap](https://github.com/twbs/bootstrap)
- [Bootstrap-Flask](https://github.com/greyli/bootstrap-flask)
- [Flask-WTF](https://github.com/lepture/flask-wtf)
- [Flask-Share](https://github.com/greyli/flask-share)
- [MyQR](https://pypi.org/project/MyQR/)
#### 书籍
- [Flask Web开发实战](https://helloflask.com)
#### 人员
- [GreyLi](https://greyli.com)

没有这些非常好的开源项目以及书籍，这个项目是不可能开发得了的。
同时，感谢GreyLi，是他的《Flask Web开发实战》带我走进了Flask世界

## 如何在本地运行这个Flask网站
1. 从Github或Gitee把项目fork到自己账户并clone下来
2. 在项目根目录中创建Python3 虚拟环境
3. 在项目根目录中运行
```bash
pip3 install -r requirements.txt
```
4. 在项目根目录中创建.env文件以及data.sqlite文件，参考config.py在.env中设置你的密码和secret_key
5. 打开flask shell并运行
```python
from .extensions import db
db.create_all()
```
6. 退出flask shell，在bash, zsh或powershell中运行`flask run`
7. 访问localhost:5000/articles，上传你自己的文章
8. 完成！现在，你可以随意修改这个项目，别忘了要把它开源哦（这个项目使用GPL3作为License）！


## 发行说明
### V3.6.0版本 2020-07-24
1. 重构代码
2. 使用CKEditor

### V3.5.0版本 2020-07-23
1. 把首页的黑底换成浅灰色底
2. 增强分页效果
3. 重构项目

### V3.4.0版本 2020-07-20
1. 给予管理员更改文章的权限
2. 用[Bootstrap-Flask](https://github.com/greyli/bootstrap-flask)以及[Bootstrap4](https://github.com/twbs/bootstrap)重构代码
3. 在首页上添加淡进效果
4. 在上传文章页面添加日期选择器

## 附注
我会有几个月的时间停止更新这个网站来学习更高级的Flask技巧。在这期间我会将网站暂时交给Rice Zong来维护
