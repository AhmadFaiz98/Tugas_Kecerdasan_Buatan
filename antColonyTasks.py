dari . antColony  mengimpor  AntColony

def  antColonyTask ():
    print ( "Harap tunggu..." )
    # diberikan beberapa node, dan beberapa lokasi...
    hd  =  3 + 5 + 2 + 4 + 2 + 7
    test_nodes  = {
        #tujuan: A, B, C, D, E, F, G, H
        "A" : ( 0 ,      6 + 9 ,     6 ,       6 + 9 + 8 ,   6 + 4 + 2 ,   3 + 2 + 4 ,   3 + 5 ,     6 + 4 + 2 + 1 ),
        "B" : ( 9 + 6 ,    0 ,       9 ,       8 ,       8 + 7 ,     9 + 4 ,     8 + 7 + 1 ,   8 + 9 ),
        "C" : ( 6 ,      9 ,       0 ,       4 + 2 + 7 ,   4 + 2 ,     4 ,       4 + 2 + 1 ,   4 + 2 + 1 ),
        "D" : ( 9 + 8 + 6 , 8 ,       7 + 2 + 4 ,   0 ,       7 ,       7 + 2 ,     7 + 1 ,     9 ),
        "E" : ( 2 + 4 + 6 , 7 + 8 ,     2 + 4 ,     7 ,       0 ,       2 ,       1 ,       1 ),
        "F" : ( 4 + 6 ,    4 + 9 ,     4 ,       2 + 7 ,     2 ,       0 ,       2 + 1 ,     2 + 1 ),
        "G" : ( 5 + 3 ,    5 + 2 + 9 ,   5 + 2 ,     1 + 7 ,     1 ,       1 + 2 ,     0 ,       3 ),
        "H" : ( 3 + 5 + 3 , 9 + 8 ,     1 + 2 + 4 ,   hd ,      1 ,       1 + 2 ,     3 ,       0 )
    }

    # ...dan fungsi untuk mendapatkan jarak antar node...
     jarak def ( mulai , akhir ):
        x_distance  =  abs ( mulai [ 0 ] -  akhir [ 0 ])
        y_distance  =  abs ( mulai [ 1 ] -  akhir [ 1 ])
        
        # c = kuadrat(a^2 + b^2)
        impor  matematika
        kembali  matematika . sqrt ( pow ( x_distance , 2 ) +  pow ( y_distance , 2 ))

    # ...kita bisa membuat koloni semut...
    koloni  =  AntColony ( test_nodes , jarak )

    # ...yang akan menemukan solusi optimal dengan ACO
    cetak ( koloni . mainloop ())
