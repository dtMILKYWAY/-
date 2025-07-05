\# “智协同”企业一体化办公平台



\*\*ZhiXieTong - An Enterprise Collaboration Platform\*\*



一个基于 Vue 3 和 Django 5 的前后端分离架构，旨在提升企业内部协作效率的现代化 OA 系统。



!\[Dashboard Screenshot](https://raw.githubusercontent.com/YOUR\_GITHUB\_USERNAME/YOUR\_REPO\_NAME/main/docs/screenshot\_dashboard.png)

\*(请将这张图片替换为你自己项目的截图)\*



---



\## ✨ 项目亮点 (Highlights)



\*   \*\*现代化技术栈\*\*: 前端采用 `Vue 3 + Vite + TypeScript + Pinia`，后端采用 `Django 5 + DRF + Simple JWT`，完全拥抱当前业界主流技术。

\*   \*\*专业的前后端分离架构\*\*: 清晰的 API 驱动模式，通过 Vite 代理解决开发环境跨域，使用 JWT 进行无状态认证。

\*   \*\*精细化权限控制\*\*: 实现了基于角色的权限系统 (RBAC)，不同角色（管理员、部门主管）拥有不同的数据可见性和操作权限。

\*   \*\*企业级 UI/UX\*\*: 对标顶级产品，设计了专业、美观、具有高级感的登录页和后台管理界面，注重用户体验细节。

\*   \*\*数据驱动的仪表盘\*\*: 提供了多图表（折线图、柱状图、仪表盘图、雷达图）的数据驾驶舱，直观展示系统核心状态。

\*   \*\*完整的核心模块\*\*: 实现了组织架构中“部门”和“员工”两个模块完整的、交互友好的 CRUD 功能。



\## 🚀 快速开始 (Quick Start)



\### 环境要求

\- Python 3.10+

\- Node.js 18+

\- MySQL 8.0+



\### 后端启动



1\.  克隆项目到本地:

&nbsp;   ```bash

&nbsp;   git clone https://github.com/YOUR\_GITHUB\_USERNAME/YOUR\_REPO\_NAME.git

&nbsp;   cd YOUR\_REPO\_NAME/backend

&nbsp;   ```

2\.  创建并激活虚拟环境:

&nbsp;   ```bash

&nbsp;   python -m venv venv

&nbsp;   source venv/bin/activate  # on Linux/macOS

&nbsp;   .\\venv\\Scripts\\activate   # on Windows

&nbsp;   ```

3\.  安装 Python 依赖:

&nbsp;   ```bash

&nbsp;   pip install -r requirements.txt

&nbsp;   ```

4\.  配置数据库:

&nbsp;   - 在 MySQL 中创建一个名为 `oa` 的空数据库。

&nbsp;   - 复制 `oaback/settings.py.example` (你需要创建一个) 为 `oaback/settings.py`，并修改其中的数据库连接信息。



5\.  执行数据库迁移和数据填充:

&nbsp;   ```bash

&nbsp;   python manage.py migrate

&nbsp;   # 如果需要初始化数据，可以创建一个 seed 命令

&nbsp;   # python manage.py seed\_data 

&nbsp;   ```

6\.  启动后端服务:

&nbsp;   ```bash

&nbsp;   python manage.py runserver

&nbsp;   ```

&nbsp;   后端服务将在 `http://127.0.0.1:8000` 启动。



\### 前端启动



1\.  进入前端目录:

&nbsp;   ```bash

&nbsp;   cd ../frontend

&nbsp;   ```

2\.  安装 Node.js 依赖:

&nbsp;   ```bash

&nbsp;   npm install

&nbsp;   ```

3\.  启动前端开发服务器:

&nbsp;   ```bash

&nbsp;   npm run dev

&nbsp;   ```

&nbsp;   前端服务将在 `http://localhost:5173` (或其他端口) 启动。



\### 默认管理员账户

\- \*\*邮箱\*\*: `dongdong@qq.com`

\- \*\*密码\*\*: `111111`



---



\## 🛠️ 技术栈 (Tech Stack)



\*   \*\*前端\*\*: Vue 3 (Composition API), Vite, TypeScript, Pinia, Vue Router, Element Plus, ECharts, Axios

\*   \*\*后端\*\*: Django 5, Django REST Framework (DRF), Simple JWT, MySQL

\*   \*\*开发工具\*\*: PyCharm/VSCode, Git, Navicat



\## 核心功能截图 (Screenshots)



\*\*登录页\*\*

!\[Login Screenshot](https://raw.githubusercontent.com/YOUR\_GITHUB\_USERNAME/YOUR\_REPO\_NAME/main/docs/screenshot\_login.png)



\*\*部门管理\*\*

!\[Department Screenshot](https://raw.githubusercontent.com/YOUR\_GITHUB\_USERNAME/YOUR\_REPO\_NAME/main/docs/screenshot\_department.png)



\*(请将这些图片替换为你自己项目的截图)\*

