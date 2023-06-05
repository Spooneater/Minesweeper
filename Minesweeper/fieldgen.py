import random
#Making an matrix[h x w]of pairs: [(mine/number of mines),[connected cells]]
def fieldgen(h,w,n):
    field = [[[0,[]] for j in range(w)]for i in range(h)]
    p = [i for i in range(h*w)]#Array of numbers, from which we randomly pick place for mines
    for i in range(n):
        num = random.randint(0,h*w-i-1)
        field[p[num] // w][p[num] % w][0] = 9#Indicator that this cell is a mine
        p.remove(p[num])
    for i in range(h):#Saving, what are subcequent cells
        for j in range(w):
            if ( i - 1 >= 0):
                if (j - 1 >=0):
                    field[i][j][1]+=[[i-1,j-1]]
                if (j+1 < w):
                    field[i][j][1]+=[[i-1,j+1]]
                field[i][j][1]+=[[i-1,j]]
            if (i+1 < h):
                if (j-1 >= 0):
                    field[i][j][1]+=[[i+1,j-1]]
                if (j+1 < w):
                    field[i][j][1]+=[[i+1,j+1]]
                field[i][j][1]+=[[i+1,j]]
            if (j - 1 >= 0):
                field[i][j][1]+=[[i,j-1]]
            if (j + 1 < w):
                field[i][j][1]+=[[i,j+1]]
    for i in range(h):
        for j in range(w):
            if field[i][j][0]!=9:
                for k in field[i][j][1]:
                    if field[k[0]][k[1]][0]==9:
                        field[i][j][0]+=1
    return field
for i in fieldgen(4,4,10):
    print(i)
