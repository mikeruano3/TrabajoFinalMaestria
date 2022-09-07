import os
c = get_config()
# Kernel config
c.IPKernelApp.pylab = 'inline'  # if you want plotting support always in your notebook
# Notebook config
c.NotebookApp.notebook_dir = 'nbs'
c.NotebookApp.allow_origin = u'cfe-jupyter.herokuapp.com' # put your public IP Address here
c.NotebookApp.ip = '*'
c.NotebookApp.allow_remote_access = True
c.NotebookApp.open_browser = False
# python -c "from notebook.auth import passwd; print(passwd())"
# ipython -c "from notebook.auth import passwd; print(passwd())"
#c.NotebookApp.password = u'argon2:$argon2id$v=19$m=10240,t=10,p=8$UM3TsL8GkVSXwiKpJxUQyw$Ju3iHr4B/xYFExcGH8KIBqrW60uXzw8GlRE7neACzh8' # ?
c.NotebookApp.password = ''
c.NotebookApp.password_required = False
c.NotebookApp.port = int(os.environ.get("PORT", 8888))
c.NotebookApp.allow_root = True
c.NotebookApp.allow_password_change = True
c.ConfigurableHTTPProxy.command = ['configurable-http-proxy', '--redirect-port', '80']