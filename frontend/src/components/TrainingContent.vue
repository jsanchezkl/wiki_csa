<template>
  <div>
    <!-- Available Courses Section -->
    <section class="mb-12" id="courses">
      <div class="flex items-center gap-3 mb-6">
        <div class="w-10 h-10 bg-purple-100 dark:bg-purple-900/30 rounded-xl flex items-center justify-center">
          <span class="material-symbols-outlined text-purple-600">menu_book</span>
        </div>
        <h2 class="text-2xl font-bold text-slate-900 dark:text-white">Available Courses</h2>
      </div>
      <div class="space-y-4">
        <div class="p-5 rounded-2xl border border-slate-100 dark:border-slate-700 bg-white dark:bg-slate-800 flex items-center gap-4 hover:shadow-md transition-shadow cursor-pointer">
          <div class="size-12 rounded-xl bg-blue-50 dark:bg-blue-900/30 flex items-center justify-center shrink-0">
            <span class="material-symbols-outlined text-blue-500">security</span>
          </div>
          <div class="flex-1">
            <h4 class="font-bold text-slate-900 dark:text-white mb-1">Security Awareness</h4>
            <p class="text-slate-500 dark:text-slate-400 text-sm">Learn about cybersecurity best practices and protecting company data.</p>
            <div class="flex items-center gap-4 mt-2">
              <span class="text-xs text-slate-400">45 min</span>
              <span class="text-xs text-slate-400">•</span>
              <span class="text-xs text-slate-400">Required</span>
            </div>
          </div>
          <span class="text-xs font-bold text-amber-600 bg-amber-50 dark:bg-amber-900/30 px-3 py-1 rounded-full shrink-0">In Progress</span>
        </div>
        <div class="p-5 rounded-2xl border border-slate-100 dark:border-slate-700 bg-white dark:bg-slate-800 flex items-center gap-4 hover:shadow-md transition-shadow cursor-pointer">
          <div class="size-12 rounded-xl bg-emerald-50 dark:bg-emerald-900/30 flex items-center justify-center shrink-0">
            <span class="material-symbols-outlined text-emerald-500">diversity_3</span>
          </div>
          <div class="flex-1">
            <h4 class="font-bold text-slate-900 dark:text-white mb-1">Diversity & Inclusion</h4>
            <p class="text-slate-500 dark:text-slate-400 text-sm">Building an inclusive workplace for everyone.</p>
            <div class="flex items-center gap-4 mt-2">
              <span class="text-xs text-slate-400">30 min</span>
              <span class="text-xs text-slate-400">•</span>
              <span class="text-xs text-slate-400">Required</span>
            </div>
          </div>
          <span class="text-xs font-bold text-emerald-600 bg-emerald-50 dark:bg-emerald-900/30 px-3 py-1 rounded-full shrink-0">Completed</span>
        </div>
        <div class="p-5 rounded-2xl border border-slate-100 dark:border-slate-700 bg-white dark:bg-slate-800 flex items-center gap-4 hover:shadow-md transition-shadow cursor-pointer">
          <div class="size-12 rounded-xl bg-purple-50 dark:bg-purple-900/30 flex items-center justify-center shrink-0">
            <span class="material-symbols-outlined text-purple-500">psychology</span>
          </div>
          <div class="flex-1">
            <h4 class="font-bold text-slate-900 dark:text-white mb-1">Leadership Essentials</h4>
            <p class="text-slate-500 dark:text-slate-400 text-sm">Develop your leadership skills and manage teams effectively.</p>
            <div class="flex items-center gap-4 mt-2">
              <span class="text-xs text-slate-400">2 hours</span>
              <span class="text-xs text-slate-400">•</span>
              <span class="text-xs text-slate-400">Optional</span>
            </div>
          </div>
          <span class="text-xs font-bold text-slate-500 bg-slate-100 dark:bg-slate-700 px-3 py-1 rounded-full shrink-0">Start</span>
        </div>
      </div>
    </section>

    <hr class="my-10 border-slate-100 dark:border-slate-700"/>

    <!-- Mandatory Training Section -->
    <section class="scroll-mt-32 mb-12" id="mandatory">
      <div class="flex items-center gap-3 mb-6">
        <div class="w-10 h-10 bg-purple-100 dark:bg-purple-900/30 rounded-xl flex items-center justify-center">
          <span class="material-symbols-outlined text-purple-600">assignment_turned_in</span>
        </div>
        <h2 class="text-2xl font-bold text-slate-900 dark:text-white">Mandatory Training</h2>
      </div>
      <p class="text-slate-600 dark:text-slate-400 mb-6">These courses must be completed within your first 30 days.</p>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="p-5 rounded-2xl bg-slate-50 dark:bg-slate-800/50 border border-slate-100 dark:border-slate-700">
          <div class="flex items-center gap-2 mb-2">
            <span class="material-symbols-outlined text-emerald-500 text-lg">check_circle</span>
            <h4 class="font-bold text-slate-900 dark:text-white">Code of Conduct</h4>
          </div>
          <p class="text-sm text-slate-500 dark:text-slate-400">Completed on Jan 15, 2024</p>
        </div>
        <div class="p-5 rounded-2xl bg-slate-50 dark:bg-slate-800/50 border border-slate-100 dark:border-slate-700">
          <div class="flex items-center gap-2 mb-2">
            <span class="material-symbols-outlined text-emerald-500 text-lg">check_circle</span>
            <h4 class="font-bold text-slate-900 dark:text-white">Diversity & Inclusion</h4>
          </div>
          <p class="text-sm text-slate-500 dark:text-slate-400">Completed on Jan 16, 2024</p>
        </div>
        <div class="p-5 rounded-2xl bg-slate-50 dark:bg-slate-800/50 border border-slate-100 dark:border-slate-700">
          <div class="flex items-center gap-2 mb-2">
            <span class="material-symbols-outlined text-amber-500 text-lg">pending</span>
            <h4 class="font-bold text-slate-900 dark:text-white">Security Awareness</h4>
          </div>
          <p class="text-sm text-slate-500 dark:text-slate-400">Due by Feb 15, 2024</p>
        </div>
        <div class="p-5 rounded-2xl bg-slate-50 dark:bg-slate-800/50 border border-slate-100 dark:border-slate-700">
          <div class="flex items-center gap-2 mb-2">
            <span class="material-symbols-outlined text-slate-400 text-lg">radio_button_unchecked</span>
            <h4 class="font-bold text-slate-900 dark:text-white">Data Privacy (GDPR)</h4>
          </div>
          <p class="text-sm text-slate-500 dark:text-slate-400">Due by Feb 15, 2024</p>
        </div>
      </div>
    </section>

    <hr class="my-10 border-slate-100 dark:border-slate-700"/>

    <!-- Certifications Section -->
    <section class="scroll-mt-32 mb-12" id="certifications">
      <div class="flex items-center gap-3 mb-6">
        <div class="w-10 h-10 bg-purple-100 dark:bg-purple-900/30 rounded-xl flex items-center justify-center">
          <span class="material-symbols-outlined text-purple-600">workspace_premium</span>
        </div>
        <h2 class="text-2xl font-bold text-slate-900 dark:text-white">Certifications</h2>
      </div>
      <p class="text-slate-600 dark:text-slate-400 mb-6">We support professional certifications with up to $2,000 annual reimbursement.</p>
      <div class="p-6 bg-gradient-to-r from-purple-50 to-indigo-50 dark:from-purple-900/20 dark:to-indigo-900/20 rounded-2xl border border-purple-100 dark:border-purple-800 mb-6">
        <div class="flex items-center gap-3 mb-3">
          <span class="material-symbols-outlined text-purple-600">info</span>
          <span class="font-bold text-slate-900 dark:text-white">How to apply for reimbursement</span>
        </div>
        <ol class="text-sm text-slate-600 dark:text-slate-400 space-y-2 list-decimal list-inside">
          <li>Submit your certification request through the HR portal</li>
          <li>Include course details and estimated cost</li>
          <li>Wait for manager approval (3-5 business days)</li>
          <li>Complete the certification and submit proof</li>
          <li>Receive reimbursement within 2 weeks</li>
        </ol>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div class="p-4 rounded-xl border border-slate-100 dark:border-slate-700 bg-white dark:bg-slate-800 text-center">
          <span class="material-symbols-outlined text-3xl text-blue-500 mb-2">cloud</span>
          <p class="text-sm font-medium text-slate-700 dark:text-slate-300">AWS Certified</p>
        </div>
        <div class="p-4 rounded-xl border border-slate-100 dark:border-slate-700 bg-white dark:bg-slate-800 text-center">
          <span class="material-symbols-outlined text-3xl text-green-500 mb-2">security</span>
          <p class="text-sm font-medium text-slate-700 dark:text-slate-300">CompTIA Security+</p>
        </div>
        <div class="p-4 rounded-xl border border-slate-100 dark:border-slate-700 bg-white dark:bg-slate-800 text-center">
          <span class="material-symbols-outlined text-3xl text-purple-500 mb-2">verified</span>
          <p class="text-sm font-medium text-slate-700 dark:text-slate-300">PMP Certification</p>
        </div>
      </div>
    </section>

    <!-- Resources Card -->
    <section class="p-6 bg-slate-900 rounded-2xl text-white overflow-hidden relative">
      <div class="relative z-10">
        <h3 class="text-xl font-bold mb-4">Learning Resources</h3>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <a class="flex items-center justify-between p-3 bg-white/10 hover:bg-white/20 rounded-xl transition-all cursor-pointer">
            <div class="flex items-center gap-3">
              <span class="material-symbols-outlined">play_circle</span>
              <span class="font-medium text-sm">LinkedIn Learning</span>
            </div>
            <span class="material-symbols-outlined">open_in_new</span>
          </a>
          <a class="flex items-center justify-between p-3 bg-white/10 hover:bg-white/20 rounded-xl transition-all cursor-pointer">
            <div class="flex items-center gap-3">
              <span class="material-symbols-outlined">library_books</span>
              <span class="font-medium text-sm">Internal Wiki</span>
            </div>
            <span class="material-symbols-outlined">chevron_right</span>
          </a>
        </div>
      </div>
      <div class="absolute -right-10 -bottom-10 w-32 h-32 bg-purple-500/30 rounded-full blur-3xl"></div>
    </section>
  </div>
</template>




