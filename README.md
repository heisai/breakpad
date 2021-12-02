# breakpad.py
## 准备依赖：
* __编译好breakpad__  

 * __make install 将编译好的库和执行文件 安装在/user/local/lib /user/local/bin 下__

## 使用：

 * __生成的dmp 文件以及 breakpad.py 和 可执行程序 放在同一个路径__
  
 * __python3 breakpad.py  可执行程序__

 * __生成 crash.log  和 error.log 查看 crash.log 即可， 脚本默认会删除dmp文件__
