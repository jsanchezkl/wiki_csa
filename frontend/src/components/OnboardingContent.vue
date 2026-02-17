<template>
  <div>
    <!-- First Week Section -->
    <section class="scroll-mt-32 mb-12" id="first-week">
      <div class="flex items-center gap-3 mb-6">
        <div class="w-10 h-10 bg-emerald-100 dark:bg-emerald-900/30 rounded-xl flex items-center justify-center">
          <span class="material-symbols-outlined text-emerald-600">calendar_today</span>
        </div>
        <h2 class="text-2xl font-bold text-slate-900 dark:text-white">Your First Week</h2>
      </div>
      <div class="space-y-4">
        <div class="p-5 rounded-2xl border border-slate-100 dark:border-slate-700 bg-white dark:bg-slate-800">
          <div class="flex items-center gap-3 mb-2">
            <span class="text-xs font-bold text-emerald-600 bg-emerald-50 dark:bg-emerald-900/30 px-2 py-1 rounded">Day 1</span>
            <h4 class="font-bold text-slate-900 dark:text-white">Welcome & Setup</h4>
          </div>
          <p class="text-slate-500 dark:text-slate-400 text-sm">Meet your team, get your equipment, and complete HR paperwork. Your buddy will guide you through the office.</p>
        </div>
        <div class="p-5 rounded-2xl border border-slate-100 dark:border-slate-700 bg-white dark:bg-slate-800">
          <div class="flex items-center gap-3 mb-2">
            <span class="text-xs font-bold text-emerald-600 bg-emerald-50 dark:bg-emerald-900/30 px-2 py-1 rounded">Day 2-3</span>
            <h4 class="font-bold text-slate-900 dark:text-white">Training Sessions</h4>
          </div>
          <p class="text-slate-500 dark:text-slate-400 text-sm">Complete mandatory training modules and learn about our company culture, values, and mission.</p>
        </div>
        <div class="p-5 rounded-2xl border border-slate-100 dark:border-slate-700 bg-white dark:bg-slate-800">
          <div class="flex items-center gap-3 mb-2">
            <span class="text-xs font-bold text-emerald-600 bg-emerald-50 dark:bg-emerald-900/30 px-2 py-1 rounded">Day 4-5</span>
            <h4 class="font-bold text-slate-900 dark:text-white">Team Integration</h4>
          </div>
          <p class="text-slate-500 dark:text-slate-400 text-sm">Shadow team members, attend your first team meeting, and start working on your first tasks.</p>
        </div>
      </div>
    </section>

    <hr class="my-10 border-slate-100 dark:border-slate-700"/>

    <!-- Tools Section -->
    <section class="scroll-mt-32 mb-12" id="tools">
      <div class="flex items-center gap-3 mb-6">
        <div class="w-10 h-10 bg-emerald-100 dark:bg-emerald-900/30 rounded-xl flex items-center justify-center">
          <span class="material-symbols-outlined text-emerald-600">build</span>
        </div>
        <h2 class="text-2xl font-bold text-slate-900 dark:text-white">Tools & Access</h2>
      </div>
      <p class="text-slate-600 dark:text-slate-400 mb-6">Here are the tools you'll need access to. IT will set these up on your first day.</p>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div class="p-4 rounded-xl border border-slate-100 dark:border-slate-700 bg-white dark:bg-slate-800 text-center">
          <span class="material-symbols-outlined text-3xl text-slate-400 mb-2">mail</span>
          <p class="text-sm font-medium text-slate-700 dark:text-slate-300">Email</p>
        </div>
        <div class="p-4 rounded-xl border border-slate-100 dark:border-slate-700 bg-white dark:bg-slate-800 text-center">
          <span class="material-symbols-outlined text-3xl text-slate-400 mb-2">chat</span>
          <p class="text-sm font-medium text-slate-700 dark:text-slate-300">Slack</p>
        </div>
        <div class="p-4 rounded-xl border border-slate-100 dark:border-slate-700 bg-white dark:bg-slate-800 text-center">
          <span class="material-symbols-outlined text-3xl text-slate-400 mb-2">folder</span>
          <p class="text-sm font-medium text-slate-700 dark:text-slate-300">Google Drive</p>
        </div>
        <div class="p-4 rounded-xl border border-slate-100 dark:border-slate-700 bg-white dark:bg-slate-800 text-center">
          <span class="material-symbols-outlined text-3xl text-slate-400 mb-2">dashboard</span>
          <p class="text-sm font-medium text-slate-700 dark:text-slate-300">Jira</p>
        </div>
      </div>
    </section>

    <hr class="my-10 border-slate-100 dark:border-slate-700"/>

    <!-- Checklist Section -->
    <section class="scroll-mt-32 mb-12" id="checklist">
      <div class="flex items-center gap-3 mb-6">
        <div class="w-10 h-10 bg-emerald-100 dark:bg-emerald-900/30 rounded-xl flex items-center justify-center">
          <span class="material-symbols-outlined text-emerald-600">checklist</span>
        </div>
        <h2 class="text-2xl font-bold text-slate-900 dark:text-white">Onboarding Checklist</h2>
      </div>
      <div class="space-y-3">
        <div class="flex items-center gap-3 p-4 border border-slate-100 dark:border-slate-700 rounded-xl bg-white dark:bg-slate-800">
          <span class="material-symbols-outlined text-emerald-500">check_circle</span>
          <span class="text-sm font-medium text-slate-700 dark:text-slate-300">Sign employment contract</span>
        </div>
        <div class="flex items-center gap-3 p-4 border border-slate-100 dark:border-slate-700 rounded-xl bg-white dark:bg-slate-800">
          <span class="material-symbols-outlined text-emerald-500">check_circle</span>
          <span class="text-sm font-medium text-slate-700 dark:text-slate-300">Complete tax forms (W-4)</span>
        </div>
        <div class="flex items-center gap-3 p-4 border border-slate-100 dark:border-slate-700 rounded-xl bg-white dark:bg-slate-800">
          <span class="material-symbols-outlined text-slate-300">radio_button_unchecked</span>
          <span class="text-sm font-medium text-slate-700 dark:text-slate-300">Set up direct deposit</span>
        </div>
        <div class="flex items-center gap-3 p-4 border border-slate-100 dark:border-slate-700 rounded-xl bg-white dark:bg-slate-800">
          <span class="material-symbols-outlined text-slate-300">radio_button_unchecked</span>
          <span class="text-sm font-medium text-slate-700 dark:text-slate-300">Enroll in benefits</span>
        </div>
        <div class="flex items-center gap-3 p-4 border border-slate-100 dark:border-slate-700 rounded-xl bg-white dark:bg-slate-800">
          <span class="material-symbols-outlined text-slate-300">radio_button_unchecked</span>
          <span class="text-sm font-medium text-slate-700 dark:text-slate-300">Complete security training</span>
        </div>
      </div>
    </section>

    <!-- Resources Card -->
    <section class="p-6 bg-slate-900 rounded-2xl text-white overflow-hidden relative">
      <div class="relative z-10">
        <h3 class="text-xl font-bold mb-4">Helpful Links</h3>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <router-link to="/wiki/policies" class="flex items-center justify-between p-3 bg-white/10 hover:bg-white/20 rounded-xl transition-all cursor-pointer">
            <div class="flex items-center gap-3">
              <span class="material-symbols-outlined">policy</span>
              <span class="font-medium text-sm">Benefits Guide</span>
            </div>
            <span class="material-symbols-outlined">chevron_right</span>
          </router-link>
          <router-link to="/wiki/training" class="flex items-center justify-between p-3 bg-white/10 hover:bg-white/20 rounded-xl transition-all cursor-pointer">
            <div class="flex items-center gap-3">
              <span class="material-symbols-outlined">school</span>
              <span class="font-medium text-sm">Training Portal</span>
            </div>
            <span class="material-symbols-outlined">chevron_right</span>
          </router-link>
        </div>
      </div>
      <div class="absolute -right-10 -bottom-10 w-32 h-32 bg-emerald-500/30 rounded-full blur-3xl"></div>
    </section>
  </div>
</template>




