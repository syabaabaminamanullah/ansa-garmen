import React, { useState, useEffect } from 'react';
import { Joyride, STATUS, EVENTS } from 'react-joyride';

export default function AppTour() {
  const [run, setRun] = useState(false);
  const [steps, setSteps] = useState([
    {
      target: '#tour-menu-superadmin',
      content: 'Selamat Datang di SEAM! Langkah pertama, klik menu Pengaturan (Super Admin) untuk memasukkan Nama Konveksi, Logo, dan Tanda Tangan Anda agar otomatis tercetak di setiap Invoice.',
      disableBeacon: true,
      title: '1. Pengaturan Perusahaan',
    },
    {
      target: '#tour-menu-master',
      content: 'Di sinilah nyawa aplikasi Anda. Masukkan data Karyawan (beserta tipe gajinya), Mitra (Supplier/Customer), dan Stok Barang (Kain/Benang) Anda di sini.',
      title: '2. Master Data',
    },
    {
      target: '#tour-menu-saldo-awal',
      content: 'Sebelum mulai transaksi, masukkan Saldo Awal Kas dan pakaian yang masih dalam proses jahit (Work in Progress) di menu ini agar pembukuan akurat.',
      title: '3. Saldo Awal',
    },
    {
      target: '#tour-menu-produksi',
      content: 'Setelah Master Data siap, gunakan menu ini setiap hari untuk mencatat pemotongan kain dan menghitung upah borongan penjahit secara otomatis.',
      title: '4. Proses Produksi',
    },
    {
      target: '#tour-menu-pembelian',
      content: 'Gunakan menu ini untuk mencatat belanja bahan baku (PO) dan biaya operasional lainnya.',
      title: '5. Pembelian & Biaya',
    },
    {
      target: '#tour-menu-penjualan',
      content: 'Gunakan menu ini untuk membuat Invoice tagihan ke pelanggan Anda.',
      title: '6. Penjualan & Tagihan',
    },
    {
      target: '#tour-menu-dashboard',
      content: 'Semua aktivitas tadi akan otomatis direkap di sini menjadi Jurnal Umum dan Laba/Rugi. Anda tinggal duduk manis dan memantau aset Anda. Selamat menggunakan SEAM!',
      title: '7. Dasbor Utama',
    }
  ]);

  useEffect(() => {
    // Cek apakah user sudah pernah menyelesaikan tour ini
    const isTourCompleted = localStorage.getItem('seam_tour_completed');
    if (!isTourCompleted) {
      // Delay sedikit agar menu di-render dulu dari API
      setTimeout(() => setRun(true), 1500);
    }
  }, []);

  const handleJoyrideCallback = (data) => {
    const { status, type } = data;
    const finishedStatuses = [STATUS.FINISHED, STATUS.SKIPPED];
    
    if (finishedStatuses.includes(status)) {
      setRun(false);
      localStorage.setItem('seam_tour_completed', 'true');
    }
  };

  return (
    <Joyride
      steps={steps}
      run={run}
      continuous={true}
      scrollToFirstStep={true}
      showProgress={true}
      showSkipButton={true}
      callback={handleJoyrideCallback}
      styles={{
        options: {
          primaryColor: '#10b981', // emerald-500
          zIndex: 10000,
          arrowColor: '#ffffff',
          backgroundColor: '#ffffff',
          textColor: '#334155',
        },
        buttonClose: {
          display: 'none',
        },
        tooltipContainer: {
          textAlign: 'left'
        },
        tooltipTitle: {
          fontSize: '16px',
          fontWeight: 'bold',
          color: '#064e3b', // emerald-900
          paddingBottom: '8px'
        },
        tooltipContent: {
          fontSize: '13px',
          lineHeight: '1.5'
        },
        buttonNext: {
          backgroundColor: '#10b981',
          fontSize: '12px',
          fontWeight: 'bold',
          padding: '8px 16px',
          borderRadius: '8px'
        },
        buttonBack: {
          color: '#64748b',
          fontSize: '12px'
        },
        buttonSkip: {
          color: '#ef4444',
          fontSize: '12px',
          fontWeight: 'bold'
        }
      }}
      locale={{
        back: 'Kembali',
        close: 'Tutup',
        last: 'Selesai',
        next: 'Lanjut',
        skip: 'Lewati Tour',
      }}
    />
  );
}

