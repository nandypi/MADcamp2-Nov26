# MAD2 demo app for bootcamp



# Commands to run the app

## Backend
1. Create virtual environment if not created
```bash
python -m venv venv
```
2. Activate virtual environment
```bash
venv/Scripts/activate #windows
source venv/bin/activate #linux
```
3. Install the packages
```bash
python -m pip list # lists all packages installed
python -m pip install requirements.txt # install whatever packages mentioned in requirement.txt file
```
4. For updating packages info
```bash
python -m pip freeze > requirements.txt
```
## Frontend
1. Change directory to frontend
```bash
cd frontend
```
2. Install packages if not 
```bash
npm install
```
3. Run the app
```bash
npm run dev
```