#
# terima kasih kepada: https://github.com/pjmattingly/ant-colony-optimization
#
# tetapi skrip ini memiliki cacat:
# AttributeError: objek 'dict_keys' tidak memiliki atribut 'hapus'
# pada baris: 36
# self.possible_locations = kemungkinan_lokasi
# yang seharusnya self.possible_locations = list(possible_locations)

dari  threading  impor  Thread

kelas  AntColony :
	kelas  semut ( Thread ):
		def  __init__ ( self , init_location , kemungkinan_lokasi , pheromone_map , distance_callback , alpha , beta , first_pass = False ):
			"""
			menginisialisasi seekor semut, untuk melintasi peta
			init_location -> menandai di mana semut mulai di peta
			kemungkinan_lokasi -> daftar kemungkinan simpul yang bisa dituju semut
				ketika digunakan secara internal, memberikan daftar kemungkinan lokasi yang dapat dilintasi semut _minus node yang sudah dikunjungi_
			pheromone_map -> peta nilai pheromone untuk setiap traversal antara setiap node
			distance_callback -> adalah fungsi untuk menghitung jarak antara dua node
			alpha -> parameter dari algoritma ACO untuk mengontrol pengaruh jumlah pheromone ketika membuat pilihan di _pick_path()
			beta -> parameter dari ACO yang mengontrol pengaruh jarak ke node berikutnya di _pick_path()
			first_pass -> jika ini adalah lintasan pertama pada peta, maka lakukan beberapa langkah secara berbeda, yang dicatat dalam metode di bawah ini
			
			rute -> daftar yang diperbarui dengan label simpul yang telah dilalui semut
			pheromone_trail -> daftar jumlah pheromone yang disimpan di sepanjang jejak semut, memetakan ke setiap lintasan dalam rute
			distance_traveled -> total jarak yang ditempuh sepanjang anak tangga dalam rute
			lokasi -> tanda di mana semut saat ini berada
			tour_complete -> bendera untuk menunjukkan bahwa semut telah menyelesaikan perjalanannya
				digunakan oleh get_route() dan get_distance_traveled()
			"""
			benang . __init__ ( sendiri )
			
			diri . init_lokasi  =  init_lokasi
			diri . kemungkinan_lokasi  =  daftar ( kemungkinan_lokasi )			
			diri . rute  = []
			diri . jarak_perjalanan  =  0,0
			diri . lokasi  =  init_lokasi
			diri . pheromone_map  =  pheromone_map
			diri . distance_callback  =  jarak_callback
			diri . alfa  =  alfa
			diri . beta  =  beta
			diri . first_pass  =  first_pass
			
			#tambahkan lokasi awal ke rute, sebelum melakukan jalan acak
			diri . _update_route ( init_location )
			
			diri . tour_complete  =  Salah
			
		def  run ( sendiri ):
			"""
			sampai self.possible_locations kosong (semut telah mengunjungi semua node)
				_pick_path() untuk menemukan node berikutnya untuk dilintasi
				_traverse() ke:
					_update_route() (untuk menampilkan traversal terbaru)
					_update_distance_traveled() (setelah traversal)
			kembalikan rute semut dan jaraknya, untuk digunakan di ant_colony:
				lakukan pembaruan feromon
				periksa kemungkinan solusi optimal baru dengan tur semut terbaru ini
			"""
			sementara  diri . kemungkinan_lokasi :
				selanjutnya  =  sendiri . _pilih_jalur ()
				diri . _traverse ( sendiri . lokasi , selanjutnya )
				
			diri . tour_complete  =  Benar
		
		def  _pick_path ( sendiri ):
			"""
			sumber: https://en.wikipedia.org/wiki/Ant_colony_optimization_algorithms#Edge_selection
			mengimplementasikan algoritma pemilihan jalur ACO
			hitung daya tarik setiap kemungkinan transisi dari lokasi saat ini
			kemudian secara acak memilih jalur berikutnya, berdasarkan daya tariknya
			"""
			#pada lintasan pertama (tanpa feromon), maka kita tinggal memilih () untuk menemukan lintasan berikutnya
			jika  diri . first_pass :
				impor  acak
				kembali  acak . pilihan ( mandiri . kemungkinan_lokasi )
			
			daya tarik  =  dict ()
			jumlah_total  =  0,0
			#untuk setiap kemungkinan lokasi, temukan daya tariknya (itu (jumlah feromon)*1/jarak [tau*eta, dari algortihm])
			#jumlahkan semua jumlah daya tarik untuk menghitung probabilitas setiap rute pada langkah berikutnya
			untuk  kemungkinan_berikutnya_lokasi  di  self . kemungkinan_lokasi :
				#CATATAN: lakukan semua perhitungan sebagai float, jika tidak, kami terkadang mendapatkan pembagian bilangan bulat karena sangat sulit untuk melacak bug
				pheromone_amount  =  float ( self . pheromone_map [ mandiri . lokasi ][ kemungkinan_lokasi_berikutnya ])
				jarak  =  float ( mandiri . distance_callback ( mandiri . lokasi , kemungkinan_berikutnya_lokasi ))
				
				#tau^alpha * eta^beta
				daya tarik [ kemungkinan_lokasi_berikutnya ] =  pow ( jumlah_feromon , self . alpha ) * pow ( 1 / jarak , self . beta )
				sum_total  +=  daya tarik [ kemungkinan_lokasi_berikutnya ]
			
			#dimungkinkan untuk memiliki nilai kecil untuk jumlah / jarak feromon, sehingga dengan kesalahan pembulatan ini sama dengan nol
			#jarang, tapi tangani saat itu terjadi
			jika  jumlah_total  ==  0.0 :
				#tambahkan semua nol, sehingga mereka adalah nilai bukan nol terkecil yang didukung oleh sistem
				#sumber: http://stackoverflow.com/a/10426033/5343977
				def  next_up ( x ):
					impor  matematika
					 struktur impor
					# NaN dan peta infinity positif untuk diri mereka sendiri.
					jika  matematika . isnan ( x ) atau ( matematika . isinf ( x ) dan  x  >  0 ):
						kembali  x

					# 0.0 dan -0.0 keduanya memetakan ke float +ve terkecil.
					jika  x  ==  0,0 :
						x  =  0,0

					n  =  struktur . membongkar ( '<q' , struct . pack ( '<d' , x ))[ 0 ]
					
					jika  n  >=  0 :
						n  + =  1
					lain :
						n  -=  1
					kembali  struktur . membongkar ( '<d' , struct . pack ( '<q' , n ))[ 0 ]
					
				untuk  kunci  daya  tarik :
					daya tarik [ key ] =  next_up ( daya tarik [ key ])
				jumlah_total  =  jumlah_berikutnya ( jumlah_total )
			
			#perilaku probabilitas kumulatif, terinspirasi oleh: http://stackoverflow.com/a/3679747/5343977
			#pilih jalur selanjutnya secara acak
			impor  acak
			lempar  =  acak . acak ()
					
			kumulatif  =  0
			untuk  kemungkinan_berikutnya_lokasi  dalam  daya tarik :
				berat  = ( daya tarik [ kemungkinan_lokasi_berikutnya ] /  jumlah_total )
				jika  lempar  <=  berat  +  kumulatif :
					kembalikan  kemungkinan_berikutnya_lokasi
				kumulatif  +=  berat
		
		def  _traverse ( mandiri , mulai , akhir ):
			"""
			_update_route() untuk menampilkan traversal baru
			_update_distance_traveled() untuk merekam jarak baru yang ditempuh
			pembaruan self.location ke lokasi baru
			dipanggil dari run()
			"""
			diri . _update_route ( akhir )
			diri . _update_distance_traveled ( awal , akhir )
			diri . lokasi  =  akhir
		
		def  _update_route ( mandiri , baru ):
			"""
			tambahkan simpul baru ke self.route
			hapus bentuk simpul baru self.possible_location
			dipanggil dari _traverse() & __init__()
			"""
			diri . rute . tambahkan ( baru )
			diri . kemungkinan_lokasi . hapus ( baru )
			
		def  _update_distance_traveled ( mandiri , mulai , akhir ):
			"""
			gunakan self.distance_callback untuk memperbarui self.distance_traveled
			"""
			diri . distance_traveled  +=  float ( self . distance_callback ( start , end ))
	
		def  get_route ( mandiri ):
			jika  diri . tur_lengkap :
				kembali  diri . rute
			kembali  Tidak ada
			
		def  get_distance_traveled ( mandiri ):
			jika  diri . tur_lengkap :
				kembali  diri . jarak_perjalanan
			kembali  Tidak ada
		
	def  __init__ ( self , node , distance_callback , start = None , ant_count = 50 , alpha = .5 , beta = 1.2 ,   pheromone_evaporation_coefficient = .40 , pheromone_constant = 10000 , , iterasi = 80 ):
		"""
		menginisialisasi koloni semut (menampung sejumlah semut pekerja yang akan melintasi peta untuk menemukan rute optimal sesuai ACO [Optimasi Koloni Semut])
		sumber: https://en.wikipedia.org/wiki/Ant_colony_optimization_algorithms
		
		node -> diasumsikan sebagai dict() yang memetakan id node ke nilai
			yang dapat dimengerti oleh distance_callback
			
		distance_callback -> diasumsikan mengambil sepasang koordinat dan mengembalikan jarak di antara mereka
			diisi ke distance_matrix pada setiap panggilan ke get_distance()
			
		start -> jika disetel, maka diasumsikan sebagai simpul tempat semua semut memulai perjalanannya
			jika tidak disetel, maka dianggap sebagai kunci simpul pertama saat diurutkan()
		
		distance_matrix -> menyimpan nilai jarak yang dihitung antar node
			diisi sesuai permintaan oleh _get_distance()
		
		pheromone_map -> menyimpan nilai akhir dari pheromone
			digunakan oleh semut untuk menentukan lintasan
			disipasi feromon terjadi pada nilai-nilai ini terlebih dahulu, sebelum menambahkan nilai feromon dari semut selama perjalanan mereka
			(di ant_updated_pheromone_map)
			
		ant_updated_pheromone_map -> matriks untuk menyimpan nilai feromon yang ditetapkan semut
			tidak digunakan untuk menghilang, nilai dari sini ditambahkan ke pheromone_map setelah langkah disipasi
			(setel ulang untuk setiap traversal)
			
		alpha -> parameter dari algoritma ACO untuk mengontrol pengaruh jumlah feromon ketika semut membuat pilihan
		
		beta -> parameter dari ACO yang mengontrol pengaruh jarak ke node berikutnya dalam pengambilan pilihan semut
		
		pheromone_constant -> parameter yang digunakan untuk menyimpan feromon di peta (Q dalam algoritma ACO)
			digunakan oleh _update_pheromone_map()
			
		pheromone_evaporation_coefficient -> parameter yang digunakan untuk menghilangkan nilai pheromone dari pheromone_map (rho dalam algoritma ACO)
			digunakan oleh _update_pheromone_map()
		
		semut -> memegang semut pekerja
			mereka melintasi peta sesuai ACO
			properti penting:
				total jarak yang ditempuh
				rute
			
		first_pass -> menandai umpan pertama untuk semut, yang memicu perilaku unik
		
		iterasi -> berapa banyak iterasi untuk membiarkan semut melintasi peta
		
		shortest_distance -> jarak terpendek dilihat dari traversal semut
		
		shortets_path_seen -> jalur terpendek dilihat dari traversal (shortest_distance adalah jarak sepanjang jalur ini)
		"""
		#simpul
		jika  tipe ( node ) bukan dict : _  
			menaikkan  TypeError ( "node harus dict" )
		
		jika  len ( node ) <  1 :
			raise  ValueError ( "harus ada setidaknya satu node di dict node" )
		
		#buat pemetaan internal dan pemetaan untuk kembali ke pemanggil
		diri . id_to_key , diri . node  =  sendiri . _init_nodes ( simpul )
		#buat matriks untuk menampung perhitungan jarak antar node
		diri . jarak_matriks  =  diri . _init_matrix ( len ( node ))
		#buat matriks untuk peta master pheromone, yang mencatat jumlah pheromone di sepanjang rute
		diri . pheromone_map  =  diri . _init_matrix ( len ( node ))
		#buat matriks untuk semut untuk menambahkan feromonnya, sebelum menambahkannya ke pheromone_map selama langkah update_pheromone_map
		diri . ant_updated_pheromone_map  =  sendiri . _init_matrix ( len ( node ))
		
		#distance_callback
		jika  tidak  dapat dipanggil ( distance_callback ):
			raise  TypeError ( "distance_callback tidak dapat dipanggil, seharusnya metode" )
			
		diri . distance_callback  =  jarak_callback
		
		#Mulailah
		jika  mulai  Tidak Ada  :
			diri . mulai  =  0
		lain :
			diri . mulai  =  Tidak ada
			#init mulai id internal dari id simpul yang dilewati
			untuk  kunci , nilai  dalam  diri . id_to_key . barang ():
				jika  nilai  ==  mulai :
					diri . mulai  =  kunci
			
			#jika kami tidak menemukan kunci di node yang dilewati, maka naikkan
			jika  diri . mulai  Tidak Ada  :
				raise  KeyError ( "Kunci: "  +  str ( start ) +  " tidak ditemukan di node yang dilewati dict." )
		
		#ant_count
		jika  tipe ( ant_count ) bukan int : _  
			menaikkan  TypeError ( "ant_count harus int" )
			
		jika  ant_count  <  1 :
			menaikkan  ValueError ( "ant_count harus >= 1" )
		
		diri . ant_count  =  ant_count
		
		#alfa	
		if ( type ( alpha ) bukan int ) dan type ( alpha ) bukan float : _  _    
			menaikkan  TypeError ( "alpha harus int atau float" )
		
		jika  alfa  <  0 :
			menaikkan  ValueError ( "alpha harus >= 0" )
		
		diri . alfa  =  mengambang ( alpha )
		
		#beta
		if ( type ( beta ) bukan int ) dan type ( beta ) bukan float : _  _    
			menaikkan  TypeError ( "beta harus int atau float" )
			
		jika  beta  <  1 :
			menaikkan  ValueError ( "beta harus >= 1" )
			
		diri . beta  =  mengambang ( beta )
		
		#feromon_evaporasi_koefisien
		jika ( type ( pheromone_evaporation_coefficient ) bukan int ) dan type ( pheromone_evaporation_coefficient ) bukan float : _  _    
			menaikkan  TypeError ( "pheromone_evaporation_coefficient harus int atau float" )
		
		diri . pheromone_evaporation_coefficient  =  mengapung ( pheromone_evaporation_coefficient )
		
		#pheromone_constant
		if ( type ( pheromone_constant ) bukan int ) dan type ( pheromone_constant ) bukan float : _  _    
			menaikkan  TypeError ( "pheromone_constant harus int atau float" )
		
		diri . pheromone_constant  =  mengambang ( pheromone_constant )
		
		#iterasi
		jika ( type ( iterasi ) bukan  int  ) :
			menaikkan  TypeError ( "iterasi harus int" )
		
		jika  iterasi  <  0 :
			menaikkan  ValueError ( "iterasi harus >= 0" )
			
		diri . iterasi  =  iterasi
		
		#init variabel internal lainnya
		diri . first_pass  =  Benar
		diri . semut  =  diri sendiri . _init_ants ( self . start )
		diri . jarak_terpendek  =  Tidak ada
		diri . shortest_path_seen  =  Tidak ada
		
	def  _get_distance ( mandiri , mulai , akhir ):
		"""
		menggunakan distance_callback untuk mengembalikan jarak antar node
		jika jarak belum dihitung sebelumnya, maka akan diisi di distance_matrix dan dikembalikan
		jika jarak telah dipanggil sebelumnya, maka nilainya dikembalikan dari distance_matrix
		"""
		jika  bukan  diri sendiri . distance_matrix [ mulai ][ akhir ]:
			jarak  =  diri . distance_callback ( self . node [ start ], self . node [ end ])
			
			if ( type ( distance ) bukan int ) dan ( type ( distance ) bukan float ) : _    
				menaikkan  TypeError ( "distance_callback harus mengembalikan int atau float, saw: " +  str ( type ( distance )))
			
			diri . distance_matrix [ mulai ][ akhir ] =  float ( jarak )
			 jarak kembali
		kembali  diri . jarak_matriks [ mulai ][ akhir ]
		
	def  _init_nodes ( self , node ):
		"""
		buat pemetaan nomor id internal (0 .. n) ke kunci di node yang dilewati
		buat pemetaan id ke nilai node
		kami menggunakan id_to_key untuk mengembalikan rute di nama node yang diharapkan pemanggil di mainloop()
		"""
		id_to_key  =  dict ()
		id_ke_nilai  =  dict ()
		
		ID  =  0
		untuk  kunci  yang  diurutkan ( node . keys ()):
			id_to_key [ id ] =  kunci
			id_to_values ​​[ id ] =  node [ key ]
			nomor  +=  1
			
		kembalikan  id_to_key , id_to_values
		
	def  _init_matrix ( diri , ukuran , nilai = 0.0 ):
		"""
		siapkan matriks NxN (di mana n = ukuran)
		digunakan di self.distance_matrix dan self.pheromone_map
		karena mereka membutuhkan matriks identik selain nilai mana yang akan diinisialisasi ke
		"""
		mundur  = []
		untuk  baris  dalam  rentang ( ukuran ):
			mundur . tambahkan ([ float ( value ) untuk  x  dalam  rentang ( size )])
		kembali  ret
	
	def  _init_ants ( mandiri , mulai ):
		"""
		pada lintasan pertama:
			membuat sejumlah objek semut
		pada lintasan berikutnya, cukup panggil __init__ pada masing-masing lintasan untuk mengatur ulang
		secara default, semua semut mulai dari simpul pertama, 0
		sesuai deskripsi masalah: https://www.codeeval.com/open_challenges/90/
		"""
		#alokasikan semut baru pada pass pertama
		jika  diri . first_pass :
			kembali [ diri . semut ( start , self . node . keys ( ), self . pheromone_map , self . _get_distance ,
				diri . alfa , diri . beta , first_pass = True ) untuk  x  dalam  jangkauan ( self . ant_count )]
		#else, setel ulang untuk digunakan pada pass lain
		untuk  semut  dalam  diri . semut :
			semut . __init__ ( mulai , self . node . keys ( ) , self . pheromone_map , self . _get_distance , self . alpha , self . beta )
	
	def  _update_pheromone_map ( sendiri ):
		"""
		1) Perbarui self.pheromone_map dengan menghilangkan nilai yang terkandung di dalamnya melalui algoritma ACO
		2) Tambahkan pheromone_values ​​dari semua semut dari ant_updated_pheromone_map
		dipanggil oleh:
			putaran utama()
			(setelah semua semut melintas)
		"""
		#selalu matriks persegi
		untuk  memulai  dalam  jangkauan ( len ( self . pheromone_map )):
			untuk  rentang akhir  ( len  ( self . pheromone_map ) ):
				#meluruhkan nilai feromon di lokasi ini
				#tau_xy <- (1-rho)*tau_xy (ACO)
				diri . pheromone_map [ start ][ end ] = ( 1 - self . pheromone_evaporation_coefficient ) * self . pheromone_map [ mulai ][ akhir ]
				
				#lalu tambahkan semua kontribusi ke lokasi ini untuk setiap semut yang melewatinya
				#(ACO)
				#tau_xy <- tau_xy + delta tau_xy_k
				# delta tau_xy_k = Q / L_k
				diri . pheromone_map [ start ][ end ] +=  self . ant_updated_pheromone_map [ mulai ][ akhir ]
	
	def  _populate_ant_updated_pheromone_map ( mandiri , semut ):
		"""
		diberi semut, isi ant_updated_pheromone_map dengan nilai pheromone sesuai ACO
		sepanjang rute semut
		dipanggil dari:
			putaran utama()
			( sebelum _update_pheromone_map() )
		"""
		rute  =  semut . get_route ()
		untuk  i  dalam  jangkauan ( len ( rute ) - 1 ):
			#temukan feromon melalui rute yang dilalui semut
			current_pheromone_value  =  float ( self . ant_updated_pheromone_map [ route [ i ]][ route [ i + 1 ]])
		
			#perbarui feromon di sepanjang bagian rute itu
			#(ACO)
			# delta tau_xy_k = Q / L_k
			new_pheromone_value  =  diri . pheromone_constant / semut . get_distance_traveled ()
			
			diri . ant_updated_pheromone_map [ route [ i ]][ route [ i + 1 ]] =  current_pheromone_value  +  new_pheromone_value
			diri . ant_updated_pheromone_map [ route [ i + 1 ]][ route [ i ]] =  current_pheromone_value  +  new_pheromone_value
		
	def  mainloop ( sendiri ):
		"""
		Menjalankan semut pekerja, mengumpulkan hasil mereka dan memperbarui peta feromon dengan nilai feromon dari pekerja
			panggilan:
			_update_pheromone()
			semut.lari()
		menjalankan waktu simulasi self.iterations
		"""
		
		untuk  _  dalam  jangkauan ( self . iterations ):
			#mulai semut multi-utas, panggil ant.run() di utas baru
			untuk  semut  dalam  diri . semut :
				semut . mulai ()
			
			#sumber: http://stackoverflow.com/a/11968818/5343977
			#tunggu sampai semut selesai, sebelum beralih ke memodifikasi sumber daya bersama
			untuk  semut  dalam  diri . semut :
				semut . bergabung ()
			
			untuk  semut  dalam  diri . semut :	
				#update ant_updated_pheromone_map dengan kontribusi feromon semut ini di sepanjang rutenya
				diri . _populate_ant_updated_pheromone_map ( semut )
				
				#jika kita belum melihat jalur apa pun, maka isi untuk perbandingan nanti
				jika  bukan  diri sendiri . jarak_terpendek :
					diri . jarak_terpendek  =  semut . get_distance_traveled ()
				
				jika  bukan  diri sendiri . shortest_path_seen :
					diri . shortest_path_seen  =  semut . get_route ()
					
				#jika kita melihat jalur yang lebih pendek, simpan untuk kembali
				jika  semut . get_distance_traveled () <  sendiri . jarak_terpendek :
					diri . jarak_terpendek  =  semut . get_distance_traveled ()
					diri . shortest_path_seen  =  semut . get_route ()
			
			#meluruhkan nilai feromon saat ini dan menambahkan semua nilai feromon yang kita lihat selama traversal (dari ant_updated_pheromone_map)
			diri . _update_pheromone_map ()
			
			#tandai bahwa kami menyelesaikan lintasan pertama semut
			jika  diri . first_pass :
				diri . first_pass  =  Salah
			
			#reset semua semut ke default untuk iterasi berikutnya
			diri . _init_ants ( self . start )
			
			#reset ant_updated_pheromone_map untuk merekam feromon untuk semut pada pass berikutnya
			diri . ant_updated_pheromone_map  =  sendiri . _init_matrix ( len ( self . node ), nilai = 0 )
		
		#terjemahkan jalur terpendek kembali ke id simpul pemanggil
		mundur  = []
		untuk  id  dalam  diri . shortest_path_seen :
			mundur . tambahkan ( self . id_to_key [ id ])
		
		kembali  ret
