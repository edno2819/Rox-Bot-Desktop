from googleapiclient.discovery import build
from google.oauth2 import service_account



def get_data_sheet():
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    SERVICE_ACCOUNT_FILE ='credentials.json'
    cred = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    SAMPLE_SPREADSHEET_ID = '1EDd0cd7BpRPNa0xs8fQxnvRpSnB4wkbEe16xnV_PrJo'
    SAMPLE_RANGE_NAME = 'A2:C50'

    service = build('sheets', 'v4', credentials=cred)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    clientes, menssagem = {}, []

    for valor in values:
        if valor==[]:
            pass
        elif len(valor)==3:
            menssagem.append(valor[2])
            if valor[0]!="":  
                clientes[valor[0]] = ''
            if valor[1]!="" and valor[0]!="":  
                clientes[valor[0]] = valor[1]

        elif len(valor)==2:
            if valor[0]!="":  
                clientes[valor[0]] = ''
            if valor[1]!="" and valor[0]!="":  
                clientes[valor[0]] = valor[1]

        else:
            if valor[0]!="":  
                clientes[valor[0]] = ''

    DATA = {'clientes':clientes, 'mensagem': menssagem}

    return DATA


