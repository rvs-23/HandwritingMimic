#!/usr/bin/env python
# coding: utf-8

# <a href = "https://www.mobilefish.com/services/record_mouse_coordinates/record_mouse_coordinates.php"> Get the coordinates!</a>

# ## Importing dependencies

# In[1]:


get_ipython().run_cell_magic('time', '', "from matplotlib import pyplot as plt\nimport numpy as np\nimport pandas as pd\nfrom matplotlib.animation import FuncAnimation\nfrom scipy import interpolate\nfrom IPython.display import HTML\n\nplt.style.use('dark_background')           #plt.style.available to see the options")


# ## Cleaning and reading the data

# In[2]:


def read_data(csv, header=None):
    df = pd.read_csv(csv, header=header)
    df.rename(columns={0:'X', 1:'Y'}, inplace=True)
    df['Xr'] = df['X'].apply(lambda x: x-df['X'].min())       # relative coordinates
    df['Yr'] = df['Y'].apply(lambda x: x-df['Y'].min())
    df_ = pd.DataFrame()
    df_['xr'] = df['Xr']
    df_['yr'] = -df['Yr']
    return df_


# In[3]:


df_ = read_data('elon.txt')                                  # rv.txt contains the coordinates
plt.plot(df_['xr'], df_['yr'], '+')


# ## Cubic B-spline curve evaluation

# In[4]:


x = df_['xr'].values
y = df_['yr'].values
  

plt.figure(figsize=(10, 8))

t = np.append([0,0,0], np.linspace(0, 1, len(x)-2, endpoint=True))
t = np.append(t, [1,1,1])                                   # knots
tck = [t, [x,y], 3]
u = np.linspace(0,1,(max(2*len(x), 50)),endpoint=True)      # For B-spline, we need a second parameter u
coordinates = interpolate.splev(u,tck)                      # evaluating the curve

plt.plot(x, y, 'r--', label='Control Polygon', marker='+', markerfacecolor='w')
plt.plot(coordinates[0], coordinates[1], 'b', linewidth=3, label='B-spline curve')
plt.legend(loc='best')
plt.axis([min(x)-50, max(x)+50, min(y)-50, max(y)+50])
plt.title('Cubic B-spline curve evaluation')
plt.show()


# ## Animation

# In[8]:


fig, ax = plt.subplots(figsize=(11,9))
ax.set(xlim=(-50, x.max()+50), ylim=(y.min()-50,50))
ax.set_title('Elon signature!!! ')
ax.grid(False)
line, = ax.plot([], [], 'b', linewidth=3)


# In[9]:


def animate(i):
    line.set_data(coordinates[0][:i], coordinates[1][:i])
    return line,

anim = FuncAnimation(fig, animate, frames=len(coordinates[0])+1, interval=20, blit=True)


# In[10]:


get_ipython().run_cell_magic('time', '', 'HTML(anim.to_html5_video())')


# In[11]:


anim.save('elon.gif', fps=25)


# In[ ]:




