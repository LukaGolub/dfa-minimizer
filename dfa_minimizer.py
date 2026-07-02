import sys
import numpy as np

class Stanje:
      def __init__(self, naziv):
        self.naziv = naziv
        self.prijelazi = []  
        self.ulazi = []
        self.prihvatljiv = False
        self.visited = False

      def dodaj_prijelaz(self, ulazni_znak, sljedeca_stanja):
             self.prijelazi.append((ulazni_znak, sljedeca_stanja))

      def dodaj_ulaz(self, ulaznoStanje):
           self.ulazi.append(ulaznoStanje)
      @staticmethod
      def get_stanje_po_imenu(stanja, ime):
       
        for stanje in stanja:
            if stanje.naziv == ime:
                return stanje
        return None
      


def dfs(stanje, posjeceni):
    
    stanje.visited = True
    posjeceni.append(stanje)
    
    
    for prijelaz in stanje.prijelazi:
        sljedeceStanje = Stanje.get_stanje_po_imenu(objekti_stanja, prijelaz[1])  # Get the next state from the transition
        if not sljedeceStanje.visited:
            dfs(sljedeceStanje, posjeceni)

def brisiNedohvatljiva(stanja, pocetno):
    posjeceni = []
    
    
    dfs(pocetno, posjeceni)
    
    
    dohvatljivi = set(posjeceni)
    
   
    
    
    stanja[:] = [stanje for stanje in stanja if stanje in dohvatljivi]

def citaj_retke():
     retci = sys.stdin.readlines()
     retci = [redak.strip() for redak in retci]
     return retci

        

retci = citaj_retke()
stanja = retci[0].split(',')
abc = retci[1].split(',')
prihv_stanja = retci[2].split(',')
poc_stanje = retci[3]     
i = 0
funk_prijelaza = []
while (4 + i) < len(retci): 
      funk_prijelaza.append(retci[4 + i])
      i += 1
objekti_stanja = [Stanje(naziv) for naziv in stanja]
for st in objekti_stanja:
     for funk in funk_prijelaza:
          trenst, trenpri = funk.split(',', 1)  
          if trenst == st.naziv:
               if trenpri.split('->')[1].split(',')[0] == trenpri.split('->')[1]: 
                  st.dodaj_prijelaz(trenpri.split('->')[0], trenpri.split('->')[1])
               else:  
                    elem = trenpri.split('->')[1].split(',')
                    brelem = len(elem)
                    i = 0
                    while i < brelem:
                         st.dodaj_prijelaz(trenpri.split('->')[0], trenpri.split('->')[1].split(',')[i])
                         i += 1

for st in objekti_stanja:
   for prijelaz in st.prijelazi:
        Stanje.get_stanje_po_imenu(objekti_stanja, prijelaz[1]).ulazi.append(st.naziv)

      
#oznaci prihvatljiva stanja    
for st in objekti_stanja:
     for ps in prihv_stanja:
          if st.naziv == ps:
               st.prihvatljiv = True


start_state = Stanje.get_stanje_po_imenu(objekti_stanja, poc_stanje)
if start_state:
    brisiNedohvatljiva(objekti_stanja, start_state)


dim = len(objekti_stanja)
matrica = np.zeros((dim, dim))
i = 0
j = 0
while i < len(objekti_stanja):
     j = 0
     while j < len(objekti_stanja):
          if objekti_stanja[i].prihvatljiv != objekti_stanja[j].prihvatljiv:
               matrica[i][j] = 1
          j+=1
     i+=1 

i = 0
j = 0
k = 0

#Minimizacija pomocu tablice, napravi tablicu gdje neznaznaceni parovi stanja se mogu minimizirati
promjena = True
while promjena:
 for i in range(len(objekti_stanja)):
    for j in range(i + 1, len(objekti_stanja)):
         if matrica[i][j] == 0:
              k = 0
              
              while k < min(len(objekti_stanja[i].prijelazi), len(objekti_stanja[j].prijelazi)):
                st1p = Stanje.get_stanje_po_imenu(objekti_stanja, objekti_stanja[i].prijelazi[k][1])
                st2p = Stanje.get_stanje_po_imenu(objekti_stanja, objekti_stanja[j].prijelazi[k][1])

                ind1 = objekti_stanja.index(st1p)
                ind2 = objekti_stanja.index(st2p)


                if matrica[ind1][ind2] == 1:
                   matrica[i][j] = 1 
                   matrica[j][i] = 1
                   promjena = True
                else: promjena = False
                k +=1
 diagonal_mask = np.eye(matrica.shape[0], dtype=bool)
 if np.all(matrica[~diagonal_mask] == 1): 
    promjena = False               
              

indStBr = []               
for i in range(len(objekti_stanja)):
    for j in range(i + 1, len(objekti_stanja)):
        
        if matrica[i][j] == 0:
            st1 = objekti_stanja[i]
            st2 = objekti_stanja[j]

            indStBr.append((j, i))

indStBr = list(set(indStBr))            

indStBr = sorted(indStBr, reverse=True)

for ind in indStBr:
 stInd = objekti_stanja[ind[0]]
 for st in objekti_stanja:
    for pr in st.prijelazi:
        if pr[1] == stInd.naziv:
            i = st.prijelazi.index(pr)
            j = objekti_stanja.index(st)
            pr = (pr[0], objekti_stanja[ind[1]].naziv)
            objekti_stanja[j].prijelazi[i] = pr
            
            
            

for i in indStBr:
    ind = i[0]
    if 0 <= ind < len(objekti_stanja) and objekti_stanja[ind] is not None:
        if objekti_stanja[ind].naziv == poc_stanje:
            poc_stanje_ind = i[1]
            poc_stanje = objekti_stanja[poc_stanje_ind].naziv
        del objekti_stanja[ind]
        if 0 <= ind < len(stanja):  
            del stanja[ind]


novaPrihv = []
for stanje in objekti_stanja:
    if stanje.prihvatljiv == True:
        novaPrihv.append(stanje)

novaPrihvTxt = []
for stanje in novaPrihv:
    novaPrihvTxt.append(stanje.naziv)
            
novaSt = ",".join(s.naziv for s in objekti_stanja)
print(novaSt)
print(",".join(abc))
print(",".join(novaPrihvTxt))
print(poc_stanje)
for stanje in objekti_stanja:
    for pri in stanje.prijelazi:
        print(f"{stanje.naziv},{pri[0]}->{pri[1]}")






                          
