import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from secret_username_and_password  import username
from secret_username_and_password  import password
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
import json
import datetime
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from secret_whatsapp_group_name import secret_group_name
from secret_cards import disabledCards
from secret_cards import onlyUseTheseCards
import re

# --- /// Functions /// ---

def initializeChromeDriverForEbonos():
    caps = webdriver.DesiredCapabilities.CHROME.copy()
    caps['acceptInsecureCerts'] = True
    caps['acceptSslCerts'] = True
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=chrome_options, desired_capabilities=caps)

def openWhatsAppWeb():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("user-data-dir=/home/notdebian/.config/google-chrome/Default")    
    return webdriver.Chrome(options=chrome_options)    
    
def sendWhatsAppWebMessage(messageToSend):
    driverWhatsapp = openWhatsAppWeb()
    driverWhatsapp.get("https://web.whatsapp.com")
    time.sleep(3)
    try:
        #whatsapp already being used somewhere else        
        useWhatsAppHereButton = WebDriverWait(driverWhatsapp, 15).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR,".\_2Zdgs .tvf2evcx")))
        useWhatsAppHereButton.click()
    except:
        try:                        
            xpathString = '//*[@title="{secret_group_name}"]'.format(secret_group_name=secret_group_name)                     
            currentSelection = driverWhatsapp.find_element(By.XPATH,xpathString).click()            
        except:
            print("could not find group")
        finally:            
            try:
                currentSelection = driverWhatsapp.find_element_by_css_selector("[title*='Type a message']")            
                time.sleep(baselineWaitInSeconds)            
                currentSelection.click()
                currentSelection.send_keys(messageToSend)
                currentSelection = driverWhatsapp.find_element(By.CSS_SELECTOR, "span[data-testid='send']").click()
                print("message sent")
                time.sleep(baselineWaitInSeconds)            
            except:
                print("could not find text input")
                time.sleep(60000)

def openWebsite():
    driver.get("http://webapp.ebonos.es/index.jsp")

def loadMainMenu():
    driver.get("https://webapp.ebonos.es/ebonos/menu.jsp")

def enterUserCredentialsAndLogIn():    
    
    username_input = driver.find_element(By.ID,"user")
    username_input.send_keys(username)
    
    password_input = driver.find_element(By.ID,"passw")
    password_input.send_keys(password)
        
    current_selector = driver.find_element(By.ID,"botonEntrar")
    current_selector.click()

def checkBrowserInstanceIsRunning():
    '''
        returns true if a browser instance is running
    '''
    if("ebonos.es" not in str(driver.current_url)):
        return False
    else:
        return True

def accessYesterdaySales():
    try:
        # --- /// IMPORTANT: needs to have delay to properly read and load the DOM /// ---
        time.sleep(baselineWaitInSeconds)    
        current_selector = driver.find_element(By.CSS_SELECTOR,".opcionKiosco .icono_atrasada")
        current_selector.click()
    except:
        # --- /// IMPORTANT: needs to have delay to properly read and load the DOM /// ---
        try:
            time.sleep(baselineWaitInSeconds)            
            current_selector = driver.find_element(By.CSS_SELECTOR,".opcionKiosco .icono_atrasada")
            current_selector.click()
        finally:
            return False

def accessTodaySales():
    try:
        # --- /// IMPORTANT: needs to have delay to properly read and load the DOM /// ---
        time.sleep(baselineWaitInSeconds)        
        current_selector = driver.find_element(By.CSS_SELECTOR,".opcionKiosco .icono_venta")
        current_selector.click()
    except:
        # --- /// IMPORTANT: needs to have delay to properly read and load the DOM /// ---
        try:
            time.sleep(baselineWaitInSeconds)            
            current_selector = driver.find_element(By.CSS_SELECTOR,".opcionKiosco .icono_venta")
            current_selector.click()
        finally:
            return False

def getCardNumberFromString(clientString):
    
    clientStringList = clientString.splitlines()    
        
    try:
        parsedName = re.search("(^\w{0,3}\s*-)?([\w\s]*)?(-|\s)?(\d*)?", clientStringList[1:][0]).group(2)
        #print(clientStringList[1:][0], "has become", found)
    except AttributeError:
        pass

    dictionaryOfClientsCardsAndNames[clientStringList[0]] = clientStringList[1:][0] = parsedName

    return clientStringList[0]

def findClientsAndReturnListOfCardNumbers():
    time.sleep(3)    
    unorderedListOfUsers = driver.find_element(By.ID,"lista_larga")    
    ebonosClients = unorderedListOfUsers.find_elements(By.TAG_NAME,"li")    
    cardNumbersAvailable = []
    for client in ebonosClients:
        cardNumber = getCardNumberFromString(client.text)        
        cardNumbersAvailable.append(cardNumber)    
    return cardNumbersAvailable

def getCurrentDateInYYMMDDFormat():
    currentDate = datetime.datetime.now()
    currentYear = currentDate.strftime("%Y")
    currentDayOfMonth = currentDate.strftime("%d")
    currentMonthOfYear = currentDate.strftime("%m")
    currentDate = currentYear+currentDayOfMonth+currentMonthOfYear
    return currentDate

def outputResultsToJSONFile(dictionaryToSave,currentDate):
    print("current:", os.listdir(os.getcwd()))

    with open("{date}_results.json".format(date=currentDate), 'wb') as fileOutput:
        json.dump(dictionaryToSave, fileOutput)        

def showCurrentSaleUserFeedback(clientCard):
    print('Procesando venta de: {clientName}'.format(clientName = dictionaryOfClientsCardsAndNames[clientCard]))

def showSalesResultsUserFeedback(listOfClientsCards):
    
    listOfSuccessfulCardsAndClientNames = []
    listOfErroredCardsAndClientNames = []
    listOfUnkownErrorsCardsAndClientNames = []

    activeCards = []
    if len(onlyUseTheseCards)>0:
        activeCards = onlyUseTheseCards
    else:
        activeCards = [clientCard for clientCard in listOfClientsCards if clientCard not in disabledCards]

    print('\n')
    for cardNumber in activeCards:
        if cardNumber in successfulSaleCards:
            listOfSuccessfulCardsAndClientNames.append("{clientName} {cardNumber}".format(clientName=dictionaryOfClientsCardsAndNames[cardNumber],cardNumber=cardNumber))
            print("Client: {clientName} with card {cardNumber} was successful".format(clientName=dictionaryOfClientsCardsAndNames[cardNumber],cardNumber=cardNumber))
        elif cardNumber in failedSaleCards:
            listOfErroredCardsAndClientNames.append("{clientName} {cardNumber}".format(clientName=dictionaryOfClientsCardsAndNames[cardNumber],cardNumber=cardNumber))
            print("Client: {clientName} with card {cardNumber} FAILED".format(clientName=dictionaryOfClientsCardsAndNames[cardNumber],cardNumber=cardNumber))
        else:
            listOfUnkownErrorsCardsAndClientNames.append("{clientName} {cardNumber}".format(clientName=dictionaryOfClientsCardsAndNames[cardNumber],cardNumber=cardNumber))
            print("Client: {clientName} with card {cardNumber} unkown error".format(clientName=dictionaryOfClientsCardsAndNames[cardNumber],cardNumber=cardNumber))
    
    print('\n')
    print("{successful} out of {total} clients were successful".format(successful=saleStatistics["Successful"], total=len(activeCards)))
    print("{errored} out of {total} clients resulted in error:".format(errored=saleStatistics["Error"], total=len(activeCards)))
    for client in listOfErroredCardsAndClientNames:
        print("     {client}".format(client=client))
    print("\n{unknown} out of {total} clients resulted in unknown".format(unknown=saleStatistics["Unknown"], total=len(activeCards)))
    for client in listOfUnkownErrorsCardsAndClientNames:
        print("     {client}".format(client=client))    

def createWhatsAppMessage(listOfClientsCards):
    
    listOfErroredCardsAndClientNames = []
    listOfUnkownErrorsCardsAndClientNames = []

    activeCards = []
    if len(onlyUseTheseCards)>0:
        activeCards = onlyUseTheseCards
    else:
        activeCards = [clientCard for clientCard in listOfClientsCards if clientCard not in disabledCards]

    for cardNumber in activeCards:        
        if cardNumber in failedSaleCards:
            listOfErroredCardsAndClientNames.append("{clientName} con numero de tarjeta {cardNumber}".format(clientName=dictionaryOfClientsCardsAndNames[cardNumber],cardNumber=cardNumber))
        elif cardNumber not in successfulSaleCards:
            listOfUnkownErrorsCardsAndClientNames.append("{clientName} con numero de tarjeta {cardNumber} ".format(clientName=dictionaryOfClientsCardsAndNames[cardNumber],cardNumber=cardNumber))
    
    stringToReturn = ""
    if(len(listOfErroredCardsAndClientNames)>0 and len(listOfUnkownErrorsCardsAndClientNames)>0):
        
        stringToReturn = 'Compraron en otro lugar:\n'
        for client in listOfErroredCardsAndClientNames:
            stringToReturn = stringToReturn+'  '+client+'\n'

        stringToReturn += 'Ha habido un error desconocido para::\n'    
        for client in listOfUnkownErrorsCardsAndClientNames:
            stringToReturn = stringToReturn+'  '+client+'\n'        
    elif(len(listOfErroredCardsAndClientNames)>0 and len(listOfUnkownErrorsCardsAndClientNames)==0):
        stringToReturn = 'Compraron en otro lugar:\n'
        for client in listOfErroredCardsAndClientNames:
            stringToReturn = stringToReturn+'  '+client+'\n'
    elif(len(listOfErroredCardsAndClientNames)==0 and len(listOfUnkownErrorsCardsAndClientNames)>0):
        stringToReturn = 'Ha habido un error desconocido para::\n'
        for client in listOfUnkownErrorsCardsAndClientNames:
            stringToReturn = stringToReturn+'  '+client+'\n'
    return stringToReturn

def executeSales(listOfClientsCards):
        activeCards = []
        if len(onlyUseTheseCards)>0:
            activeCards = onlyUseTheseCards
        else:
            activeCards = [clientCard for clientCard in listOfClientsCards if clientCard not in disabledCards]
        
        print('\n', 'Using only these cards: ', activeCards, '\n' )

        for activeCard in activeCards:            
            try:                
                
                WebDriverWait(driver, 120).until(expected_conditions.presence_of_element_located((By.ID,activeCard)))

                showCurrentSaleUserFeedback(activeCard)

                #find client selector                
                currentClientSelection = driver.find_element(By.ID,activeCard)
                currentClientSelection.click()
                time.sleep(baselineWaitInSeconds)

                #double click over client
                actionchains = ActionChains(driver)        
                actionchains.double_click(currentClientSelection).perform()
                time.sleep(baselineWaitInSeconds)        
                                
                #accept alert
                Alert(driver).accept()
                time.sleep(baselineWaitInSeconds)
                
                ''''''
                try:
                    errorString = 0
                    # check if the sale was successful or not                    
                    
                    currentSelection = driver.find_element(By.CLASS_NAME,"notification_fail_p2")                    

                    if "Ha alcanzado el numero maximo de ejemplares retirados para el dia. Para mas informacion pongase en contacto con su publicacion" in currentSelection.text:
                        errorString = "Ya ha sido cobrado"
                    elif "No se encuentra suscripcion para la tarjeta proporcionada. Para mas informacion pongase en contacto con su publicacion" in currentSelection.text:
                        errorString = "Tarjeta inactiva"
                    elif "No tiene activada la entrega de ejemplares para el dia. Para mas informacion pongase en contacto con su publicacion" in currentSelection.text:
                        errorString = "Tarjeta inactiva para el dia seleccionado"
                    elif "La tarjeta esta inactiva para la suscripcion. Para mas informacion pongase en contacto con su publicacion":
                        errorString = "Tarjeta inactiva"
                    else:
                        errorString = "Unknown, check screencapture"  
                        driver.save_screenshot("screenshot_error_{date}_{client_card_number}.png".format(date=getCurrentDateInYYMMDDFormat(),client_card_number=activeCard))
                        print("An unknown error has occurred while processing the sale for: ", activeCard , dictionaryOfClientsCardsAndNames[activeCard])
                        print('\n Error:', e)
                        saleStatistics["Unknown"] += 1
                                        
                    failedSaleCards.append(activeCard)
                    saleStatistics["Error"] += 1

                    if errorString==0:
                        raise NameError(errorString)
                    else:
                        continue

                except Exception as e:
                    try:         
                        
                        # if there are multiple items for sale - > confirm all
                        
                        time.sleep(baselineWaitInSeconds+1)                        
                        currentSelection = driver.find_element(By.ID,"boton_central")                        
                        currentSelection.click()
                        
                        successfulSaleCards.append(activeCard)                        
                        saleStatistics["Successful"] += 1
                        
                        time.sleep(baselineWaitInSeconds)

                    except Exception as e:                        
                        try:                            
                            # item for sale has an associated promotion                            

                            time.sleep(baselineWaitInSeconds)
                            time.sleep(baselineWaitInSeconds/2)
                            currentSelection = driver.find_element(By.ID,"boton_pedidos")                            
                            currentSelection.click()                            
                            successfulSaleCards.append(activeCard)
                            saleStatistics["Successful"] += 1
                            time.sleep(baselineWaitInSeconds)
                            time.sleep(baselineWaitInSeconds)
                        except Exception as e:                    
                            try:                                
                                # sale was completed on the first try
                                time.sleep(baselineWaitInSeconds)
                                time.sleep(baselineWaitInSeconds/2)                                
                                # checking that the successfult sale result message exists
                                currentSelection = driver.find_element(By.CLASS_NAME,"resultado_venta")                                
                                successfulSaleCards.append(activeCard)
                                saleStatistics["Successful"] += 1                            
                                time.sleep(baselineWaitInSeconds/2)                                
                            except Exception as e:
                                print("An unknown error has occurred while processing the sale for: ", activeCard , dictionaryOfClientsCardsAndNames[activeCard])
                                print('\n Error:', e)
                            finally:
                                continue
                    finally:
                        continue
                finally:                    
                    try:
                        WebDriverWait(driver, 240).until(expected_conditions.presence_of_element_located((By.CLASS_NAME,"icono_flecha")))

                        #go back to main menu
                        
                        time.sleep(baselineWaitInSeconds)                        
                        firstholder = driver.find_element(By.CLASS_NAME,"icono_flecha")
                        firstholder.click()                          

                    except Exception as e:                                            
                        loadMainMenu()                    
                        print('\n Error:', e)
                    
            except Exception as e:
                driver.save_screenshot("screenshot_error_{date}_{client_card_number}.png".format(date=getCurrentDateInYYMMDDFormat(),client_card_number=activeCard))
                print("An unknown error has occurred while processing the sale for: ", activeCard , dictionaryOfClientsCardsAndNames[activeCard])
                print('\n Error:', e)
                saleStatistics["Unknown"] += 1
            finally:                
                continue

# --- /// Global variables /// ---

dictionaryOfClientsCardsAndNames = {}
 
saleStatistics = {'Successful':0,'Error':0,'Unknown':0}

baselineWaitInSeconds = 2

successfulSaleCards = []
failedSaleCards = []

e = 'start'

driver = initializeChromeDriverForEbonos()

# ------------------ /// MAIN /// ------------------

print("\n ========================================================================= \n")

if len(onlyUseTheseCards)>0:
    print("*** WARNING ***: will only process the following cards: ", onlyUseTheseCards)
    confirmation = input("Are you sure? Enter yes/no [Y/n]")
    if confirmation == "n" or confirmation == "N":
        quit()
    elif confirmation != "y" and confirmation != "Y":
        quit()


if len(disabledCards)>0:
    print("*** WARNING ***: will the following cards will NOT be processed: ", disabledCards)
    confirmation = input("Are you sure? Enter yes/no [Y/n]")
    if confirmation == "n" or confirmation == "N":
        quit()
    elif confirmation != "y" and confirmation != "Y":
        quit()

print("\n ========================================================================= \n")
desiredDate = input("Enter 1 to execute today's sales, enter 2 to execute yesterday's sales or enter a specific date in the format yy/mm/dd \nEnter your answer here: ")
try:
    desiredDate = int(desiredDate)
except:
    print("Error occurred while converting input")
    quit()

openWebsite()
enterUserCredentialsAndLogIn()
if desiredDate == 1:
    print("\n Processing sales for TODAY")
    accessTodaySales()
else:
    print("\n Processing sales for YESTERDAY")
    accessYesterdaySales()

listOfClientsCards = findClientsAndReturnListOfCardNumbers()    
executeSales(listOfClientsCards)    
showSalesResultsUserFeedback(listOfClientsCards)
messageToSend=createWhatsAppMessage(listOfClientsCards)
sendWhatsAppWebMessage(messageToSend)

    