ARG ODOO_VERSION=lastest

FROM odoo:${ODOO_VERSION}

COPY . .

RUN python3 -m pip install -r requirements.txt --break-system-packages 
