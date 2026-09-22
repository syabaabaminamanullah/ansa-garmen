# ANSA - ERP (Raziq Garment)

Sistem ERP manajemen operasional garmen, persediaan bahan baku, proses produksi (cutting, jahit/makloon, finishing), penggajian karyawan borongan/tetap, dan pencatatan keuangan akuntansi untuk Raziq Garment.

## Fitur Utama
- **Master Data & Inventori**: Manajemen bahan baku (kain), bahan pembantu/penolong, dan barang jadi dengan kode SKU & model code.
- **Produksi**: Pencatatan log produksi per divisi (Cutting, Jahit/Makloon, Finishing & QC).
- **Penggajian**: Sistem kalkulasi upah borongan (per pcs) maupun mingguan/bulanan.
- **Keuangan & Akuntansi**: Jurnal umum, COA (Bagan Akun Standar), neraca, dan laporan laba rugi.
- **Generator Dokumen**: Export otomatis faktur penjualan, PO pembelian, surat jalan, dan slip gaji ke format PDF.

## Tech Stack
- **Backend**: FastAPI / Python
- **Database**: PostgreSQL (Supabase) / SQLite (Development)
- **Deployment**: Vercel / Railway
