
###pseudo protocals digger 伪协议查看工具

  搜索系统支持的伪协议,目前仅支持Windows ..

###How to using

  Windows 关于伪协议的程序调用在注册表里面保存,这个工具的用途是快速检索出伪协议的名称和对应的程序路径,脚本只需要直接运行便可以得出结果<br/>
  
  ![run](https://raw.githubusercontent.com/lcatro/pseudo-protocals-digger/master/pic/run.png)<br/>
  
###Example
  
  系统上支持QQPet 的伪协议,于是来分析下能不能利用<br/>
  
  ![example](https://raw.githubusercontent.com/lcatro/pseudo-protocals-digger/master/pic/example.png)<br/>
  
  在IE 上的地址栏输入(**QQPet://**) ,可以看到IE 会尝试调用伪协议对应的程序<br/>
  
  ![try_execute](https://raw.githubusercontent.com/lcatro/pseudo-protocals-digger/master/pic/try_execute.png)<br/>
  
  使用IDA 分析,找到WinMain() 开始分析,看到下面代码<br/>
  
  ![resolve](https://raw.githubusercontent.com/lcatro/pseudo-protocals-digger/master/pic/resolve.png)<br/>
  
  现在我们知道这个伪协议的格式为:QQPet://$smartloader$  ($product$  (123)$qq$  (1234567)$fullname$  (ismyname)$extra$  (123)) 
  继续往下阅读代码,伪协议执行程序会判断**product** ,**fullname** ,**extra** 是否为有效字符,然后自己构造一个参数列表,准备传递给接下来要运行的程序<br/>
  
  ![valid](https://raw.githubusercontent.com/lcatro/pseudo-protocals-digger/master/pic/valid.png)<br/>
  
  ![valid_](https://raw.githubusercontent.com/lcatro/pseudo-protocals-digger/master/pic/valid_.png)<br/>
  
  从配置文件中获取准备要运行的程序路径,然后判断这个程序能否被访问,最后调用CreateProcess 运行<br/>
  
  ![version_and_path](https://raw.githubusercontent.com/lcatro/pseudo-protocals-digger/master/pic/version_and_path.png)<br/>
  
  然后我们找到两个配置文件的路径,一个是原来路径下的kernelInfo.ini (C:\Program Files (x86)\Tencent\QQ\Plugin\Com.Tencent.QQPet\bin\QQPet),
  另一个是kernel.ini (C:\Documents and Settings\All Users\Application Data\QQPet\Registrar)<br/>
  
  ![kernel](https://raw.githubusercontent.com/lcatro/pseudo-protocals-digger/master/pic/kernel.png)<br/>
  
  在分析QQPetKernelBeta16Build001.exe 的过程中,发现有一个地方可以增加一项目kernel.ini 的配置<br/>
  
  ![add_item](https://raw.githubusercontent.com/lcatro/pseudo-protocals-digger/master/pic/add_item.png)<br/>
  
  查看上一调用可以看到这里传入了一个字符串<br/>
  
  ![add_item_](https://raw.githubusercontent.com/lcatro/pseudo-protocals-digger/master/pic/add_item_.png)<br/>
  
  再往上看,可以知道这个是解析参数中的/n 参数的值,所以可以知道,只要控制了/n ,那么也就可以控制kernel.ini 新建的item <br/>
  
  ![product_string](https://raw.githubusercontent.com/lcatro/pseudo-protocals-digger/master/pic/product_string.png)<br/>
  
  由上面的分析可以知道,/n 对应的是$product$ 的参数,于是构造payload QQPet://$smartloader$  ($product$  (123)$fullname$  (1)$extra$  (1)) ,在IE 执行这段伪协议,发现kernel.ini 添加了新的item <br/>
  
  ![new_item](https://raw.githubusercontent.com/lcatro/pseudo-protocals-digger/master/pic/new_item.png)<br/>
  
  同样地,我们也可以把原来Kernel 的那项SetupPath 替换掉,payload QQPet://$smartloader$  ($product$  (Kernel)$fullname$  (1)$extra$  (1)) <br/>
  
  ![rewrite](https://raw.githubusercontent.com/lcatro/pseudo-protocals-digger/master/pic/rewrite.png)<br/>
  
  