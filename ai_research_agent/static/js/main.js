/* ==========================================================================
   AI Research Assistant Agent - Global Frontend Scripts
   ========================================================================== */

document.addEventListener("DOMContentLoaded", () => {
    // 1. Sidebar Toggle for Mobile Views
    const sidebar = document.getElementById("appSidebar");
    const toggleBtn = document.getElementById("sidebarToggle");
    
    if (toggleBtn && sidebar) {
        toggleBtn.addEventListener("click", (e) => {
            e.stopPropagation();
            sidebar.classList.toggle("open");
        });
        
        // Close sidebar when clicking outside on mobile
        document.addEventListener("click", (e) => {
            if (sidebar.classList.contains("open") && !sidebar.contains(e.target) && e.target !== toggleBtn) {
                sidebar.classList.remove("open");
            }
        });
    }

    // 2. Global Header Theme Toggle
    const themeBtn = document.getElementById("themeToggle");
    if (themeBtn) {
        themeBtn.addEventListener("click", () => {
            const currentTheme = document.documentElement.getAttribute("data-theme") || "dark";
            const newTheme = currentTheme === "dark" ? "light" : "dark";
            
            // Apply theme changes to document instantly
            document.documentElement.setAttribute("data-theme", newTheme);
            
            // Persist the selection to backend session (if logged in)
            fetch("/dashboard/settings/theme", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ theme: newTheme })
            })
            .then(res => res.json())
            .then(data => {
                if (data.status === "success") {
                    showToast(`Theme switched to ${newTheme} mode.`, "info");
                    // If dashboard theme buttons exist, update their status too
                    if (typeof updateSettingsThemeButtons === "function") {
                        updateSettingsThemeButtons(newTheme);
                    }
                }
            })
            .catch(err => {
                // If not logged in, we still toggle but don't flash errors
                console.log("Offline theme toggle applied.");
            });
        });
    }
});

// 3. Dynamic Toast Notification System
function showToast(message, type = "info") {
    const container = document.getElementById("toastContainer");
    if (!container) return;

    // Map types to Lucide icon tags
    let iconName = "info";
    if (type === "success") iconName = "check-circle";
    if (type === "error") iconName = "alert-triangle";

    const toast = document.createElement("div");
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <i data-lucide="${iconName}"></i>
        <span>${message}</span>
    `;

    container.appendChild(toast);
    
    // Refresh icons inside new toast
    if (window.lucide) {
        lucide.createIcons({
            attrs: {
                class: 'toast-icon'
            }
        });
    }

    // Auto-remove after 4 seconds
    setTimeout(() => {
        toast.style.transition = "opacity 0.5s, transform 0.5s";
        toast.style.opacity = "0";
        toast.style.transform = "translateY(10px)";
        setTimeout(() => toast.remove(), 500);
    }, 4000);
}
