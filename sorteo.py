import time

dict=[
{
"Nombre":"Leo",
"Apellido":"Lorenzo",
"Edad":18    
},
{
"Nombre":"Manuel",
"Apellido":"Ramirez"     ,
"Edad":15   
},
{
"Nombre":"Peppa ",
"Apellido":"pig"     ,
"Edad":20   
},
{
"Nombre":"jeje leo",
"Apellido":"sknda"     ,
"Edad":14  
},
]
word="Leo"
info=[{"Nombre":item['Nombre'],"Apellido":item['Apellido']} for item in dict if word.lower() in item["Nombre"].lower()]

print(info)
# dict2=[{"Nombre":item['Nombre'],"Apellido":item['Apellido']}
#                for item in dict if int(item['Edad'])
#                >=18]



