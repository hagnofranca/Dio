salario = float(input()) 

def novo_salario(salario, reajuste):
  return (f" Novo salario: {(salario * (1 + (reajuste/100))):.2f}\n Reajuste ganho: {(salario * (reajuste/100)):.2f}\n Em percentual: {reajuste} %")

if ( salario <= 600.00 ):
  print (novo_salario(salario, 17))
elif ( 600 < salario <= 900.00 ):
  print (novo_salario(salario, 13))
elif ( 900.00 < salario <= 1500.00):
  print (novo_salario(salario,12))
elif ( 1500.00 < salario <= 2000.00  ):
  print (novo_salario(salario,10))
else: 
  print (novo_salario(salario,5))
