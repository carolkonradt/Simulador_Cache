import math
import numpy as np
from bitstring import BitArray
import bitarray
import random
import sys

def main():
    print("cache_simulator <nsets> <bsize> <assoc> <substituição> <flag_saida> arquivo_de_entrada")
    
    linha_de_comando = input()
    command_line = linha_de_comando.split()
    
    if len(command_line)!=7:
        print("Sua linha de código não possui os parâmetros corretos. Tente novamente! ")
        sys.exit()

    acessos=-1
    cache_name = command_line[0]
    nsets= int(command_line[1])
    bsize = int(command_line[2])
    assoc = int(command_line[3])
    subst = command_line[4]
    flag = int(command_line[5])
    arquivo_nome = command_line[6]
    hit =0
    miss_compulsorio=0
    miss_capacidade=0
    miss_conflito=0
    capacidade_total=0
    #print(cache_name, nsets, bsize, assoc, subst, flag, arquivo)

    #------------------- identifica numero de bits de cada parametro --------------------
    n_bits_offset = int(math.log2(bsize))#bsize
    n_bits_indice = int(math.log2(nsets)) #nsets
    n_bits_tag = 32-n_bits_offset-n_bits_indice

    #------------------- cria vetores para cache ------------------
    cache_val=[0 for i in range(assoc*nsets)]
    cache_tag=[0 for i in range(assoc*nsets)]
    cache_ca_val = constroiMatriz(nsets, assoc)
    cache_ca_tag = constroiMatriz(nsets, assoc)

    try:
        with open(arquivo_nome, "rb") as arquivo: # Abertura do arquivo apenas leitura
            chunk_size=4 #chunk_size significa numero de bytes lidos

            while True:
                chunk=arquivo.read(chunk_size) #lê de 4 em 4 bytes
                acessos+=1 
                
                if not chunk: #quando acabar os endereços, para de ler
                    break
                
                inteiro = int.from_bytes(chunk)
                tag = inteiro >> (n_bits_offset + n_bits_indice)
                indice = (inteiro >> n_bits_offset) & (2**(n_bits_indice)-1)

                #escolhemos utilizar o inteiro para facilitar o código

        #------------------ mapeamento direto --------------
        #está sem miss de capacidade
                if assoc==1: 
                    if cache_val[indice]==0:
                        miss_compulsorio+=1
                        cache_val[indice]=1
                        cache_tag[indice]=tag
                    
                    elif cache_tag[indice]==tag:
                        hit+=1
                    
                    else:
                        miss_conflito+=1
                        cache_val[indice]=1
                        cache_tag[indice]=tag

        #--------------- totalmente associativo ------------------- FEITO
                elif nsets==1:
                    capacidade=0
                    for i in range(assoc): #equivalente em C: for(i=0; i<assoc; i++)
                        if cache_val[i]==0:
                            miss_compulsorio+=1
                            cache_val[i]=1
                            cache_tag[i]=tag
                            break
                        
                        elif cache_tag[i]==tag:
                            hit+=1
                            break
                        
                        else:
                            capacidade+=1
                    
                    if capacidade==assoc:
                        miss_capacidade+=1
                        num_substituicao = subst_random(assoc)
                        cache_val[num_substituicao]=1
                        cache_tag[num_substituicao]=tag

        #---------------------conjunto associativa---------------------
        #está sem miss de conflito
                else:
                    capacidade_via=0
                    for i in range(assoc):
                        if cache_ca_val[indice][i]==0:
                            miss_compulsorio+=1
                            cache_ca_val[indice][i]=1
                            cache_ca_tag[indice][i]=tag
                            capacidade_total+=1

                            break

                        elif cache_ca_tag[indice][i]==tag:
                            hit+=1
                            break

                        else:
                            capacidade_via+=1

                    if capacidade_via==assoc and capacidade_total ==(assoc*nsets):
                        miss_capacidade+=1
                        num_substituicao = subst_random(assoc)
                        cache_ca_val[indice][num_substituicao]=1
                        cache_ca_tag[indice][num_substituicao]=tag

                    elif capacidade_via==assoc and capacidade_total!=(assoc*nsets):
                        miss_conflito+=1
                        num_substituicao=subst_random(assoc)
                        cache_ca_val[indice][num_substituicao]=1
                        cache_ca_tag[indice][num_substituicao]=tag

    except:
        print("Erro na leitura de arquivo. Tente novamente!")
        sys.exit()
        
    total_misses = miss_compulsorio+miss_capacidade+miss_conflito

    if flag==1:
        print(acessos, round((hit/acessos), 2), round((total_misses/acessos), 2), round((miss_compulsorio/total_misses), 2), round((miss_capacidade/total_misses), 2), round((miss_conflito/total_misses), 2))

    else:
        print("Taxa de hit: ", hit/acessos, "\nTaxa de miss: ", total_misses/acessos) 

def subst_random(max):
    return (random.randint(0, max-1))

def constroiMatriz(conjuntos, associatividade):
    matriz = []
    for i in range(conjuntos):
        list.append(matriz,[0]*associatividade)
    return matriz

if __name__ == "__main__":
    main()


