<template>
  <div>
    <!-- Health Insurance Section -->
    <section class="scroll-mt-32 mb-12" id="health-insurance">
      <div class="flex items-center gap-3 mb-6">
        <div class="w-10 h-10 bg-primary/10 rounded-xl flex items-center justify-center">
          <span class="material-symbols-outlined text-primary">health_and_safety</span>
        </div>
        <h2 class="text-2xl font-bold text-slate-900 dark:text-white">Health Insurance</h2>
      </div>
      <p class="text-slate-600 dark:text-slate-400 mb-6">We provide comprehensive health coverage for all full-time employees starting from day one.</p>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <div class="p-5 rounded-2xl border border-slate-100 dark:border-slate-700 bg-white dark:bg-slate-800">
          <span class="material-symbols-outlined text-primary mb-3">medical_services</span>
          <h4 class="font-bold text-slate-900 dark:text-white mb-2">Medical Coverage</h4>
          <p class="text-slate-500 dark:text-slate-400 text-sm">PPO and HDHP plans available with 90% employer-paid premiums.</p>
        </div>
        <div class="p-5 rounded-2xl border border-slate-100 dark:border-slate-700 bg-white dark:bg-slate-800">
          <span class="material-symbols-outlined text-primary mb-3">dentistry</span>
          <h4 class="font-bold text-slate-900 dark:text-white mb-2">Dental & Vision</h4>
          <p class="text-slate-500 dark:text-slate-400 text-sm">Full dental and vision coverage included at no additional cost.</p>
        </div>
      </div>
    </section>

    <hr class="my-10 border-slate-100 dark:border-slate-700"/>

    <!-- Time Off Section -->
    <section class="scroll-mt-32 mb-12" id="time-off">
      <div class="flex items-center gap-3 mb-6">
        <div class="w-10 h-10 bg-primary/10 rounded-xl flex items-center justify-center">
          <span class="material-symbols-outlined text-primary">beach_access</span>
        </div>
        <h2 class="text-2xl font-bold text-slate-900 dark:text-white">Time Off Policy</h2>
      </div>
      <p class="text-slate-600 dark:text-slate-400 mb-6">We believe in work-life balance and offer flexible time off policies.</p>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="p-5 rounded-2xl bg-slate-50 dark:bg-slate-800/50 border border-slate-100 dark:border-slate-700">
          <h4 class="font-bold text-primary mb-2">Paid Time Off</h4>
          <p class="text-sm text-slate-600 dark:text-slate-400">20 days PTO per year, increasing with tenure.</p>
        </div>
        <div class="p-5 rounded-2xl bg-slate-50 dark:bg-slate-800/50 border border-slate-100 dark:border-slate-700">
          <h4 class="font-bold text-primary mb-2">Sick Leave</h4>
          <p class="text-sm text-slate-600 dark:text-slate-400">Unlimited sick days - your health comes first.</p>
        </div>
        <div class="p-5 rounded-2xl bg-slate-50 dark:bg-slate-800/50 border border-slate-100 dark:border-slate-700">
          <h4 class="font-bold text-primary mb-2">Holidays</h4>
          <p class="text-sm text-slate-600 dark:text-slate-400">12 company holidays plus winter break closure.</p>
        </div>
        <div class="p-5 rounded-2xl bg-slate-50 dark:bg-slate-800/50 border border-slate-100 dark:border-slate-700">
          <h4 class="font-bold text-primary mb-2">Parental Leave</h4>
          <p class="text-sm text-slate-600 dark:text-slate-400">16 weeks fully paid parental leave.</p>
        </div>
      </div>
    </section>

    <hr class="my-10 border-slate-100 dark:border-slate-700"/>

    <!-- Retirement Section -->
    <section class="scroll-mt-32 mb-12" id="retirement">
      <div class="flex items-center gap-3 mb-6">
        <div class="w-10 h-10 bg-primary/10 rounded-xl flex items-center justify-center">
          <span class="material-symbols-outlined text-primary">savings</span>
        </div>
        <h2 class="text-2xl font-bold text-slate-900 dark:text-white">Retirement Benefits</h2>
      </div>
      <p class="text-slate-600 dark:text-slate-400 mb-6">Plan for your future with our competitive retirement benefits.</p>
      <ul class="grid grid-cols-1 md:grid-cols-2 gap-3">
        <li class="flex gap-3 p-4 border border-slate-100 dark:border-slate-700 rounded-xl items-center bg-white dark:bg-slate-800">
          <span class="material-symbols-outlined text-green-500">check_circle</span>
          <span class="text-sm font-medium text-slate-700 dark:text-slate-300">401(k) with 4% company match</span>
        </li>
        <li class="flex gap-3 p-4 border border-slate-100 dark:border-slate-700 rounded-xl items-center bg-white dark:bg-slate-800">
          <span class="material-symbols-outlined text-green-500">check_circle</span>
          <span class="text-sm font-medium text-slate-700 dark:text-slate-300">Immediate vesting</span>
        </li>
        <li class="flex gap-3 p-4 border border-slate-100 dark:border-slate-700 rounded-xl items-center bg-white dark:bg-slate-800">
          <span class="material-symbols-outlined text-green-500">check_circle</span>
          <span class="text-sm font-medium text-slate-700 dark:text-slate-300">Financial planning resources</span>
        </li>
        <li class="flex gap-3 p-4 border border-slate-100 dark:border-slate-700 rounded-xl items-center bg-white dark:bg-slate-800">
          <span class="material-symbols-outlined text-green-500">check_circle</span>
          <span class="text-sm font-medium text-slate-700 dark:text-slate-300">Stock options available</span>
        </li>
      </ul>
    </section>

    <!-- Resources Card -->
    <section class="p-6 bg-slate-900 rounded-2xl text-white overflow-hidden relative">
      <div class="relative z-10">
        <h3 class="text-xl font-bold mb-4">Related Documents</h3>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <a class="flex items-center justify-between p-3 bg-white/10 hover:bg-white/20 rounded-xl transition-all cursor-pointer">
            <div class="flex items-center gap-3">
              <span class="material-symbols-outlined">description</span>
              <span class="font-medium text-sm">Benefits Guide 2024.pdf</span>
            </div>
            <span class="material-symbols-outlined">download</span>
          </a>
          <a class="flex items-center justify-between p-3 bg-white/10 hover:bg-white/20 rounded-xl transition-all cursor-pointer">
            <div class="flex items-center gap-3">
              <span class="material-symbols-outlined">description</span>
              <span class="font-medium text-sm">Employee Handbook.pdf</span>
            </div>
            <span class="material-symbols-outlined">download</span>
          </a>
        </div>
      </div>
      <div class="absolute -right-10 -bottom-10 w-32 h-32 bg-primary/30 rounded-full blur-3xl"></div>
    </section>
  </div>
</template>




