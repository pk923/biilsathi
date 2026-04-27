import re
import sys

def main():
    templates_str = """var TEMPLATES = {
            product: [
                { id: 'p1', name: 'Modern Retail Invoice', desc: 'Wave gradient — clothing & fashion shops', badge: 'Popular', badgeColor: '#5b3fff', fields: ['Product', 'Qty', 'Price', 'GST', 'Total'], accent: '#5b3fff' },
                { id: 'p2', name: 'Electronics Shop Invoice', desc: 'Dark header with contact bar & status', badge: 'New', badgeColor: '#0288d1', fields: ['Product', 'Qty', 'Price', 'Total'], accent: '#0288d1' },
                { id: 'p3', name: 'GST Product Invoice', desc: 'Full CGST / SGST compliance columns', badge: 'GST', badgeColor: '#6366f1', fields: ['HSN', 'Taxable', 'CGST', 'SGST', 'Total'], accent: '#6366f1' },
                { id: 'p4', name: 'Minimal Store Invoice', desc: 'Classic serif elegant design', badge: null, badgeColor: null, fields: ['Item', 'Qty', 'Rate', 'Total'], accent: '#334155' },
                { id: 'p5', name: 'Wholesale Invoice', desc: 'Side accent strip with 5% discount column', badge: 'B2B', badgeColor: '#6d28d9', fields: ['Product', 'Qty', 'Rate', 'Disc', 'Total'], accent: '#6d28d9' },
                { id: 'p6', name: 'Luxury Retail Invoice', desc: 'Gold + black premium style', badge: 'Premium', badgeColor: '#d4af37', fields: ['Item', 'Qty', 'Price', 'GST', 'Total'], accent: '#d4af37' },
                { id: 'p7', name: 'Grocery Fast Billing', desc: 'Clean green retail style', badge: 'Fast', badgeColor: '#16a34a', fields: ['Product', 'Qty', 'Rate', 'Tax', 'Total'], accent: '#16a34a' },
                { id: 'p8', name: 'Electronics Neon', desc: 'Dark + blue modern tech style', badge: 'Modern', badgeColor: '#0ea5e9', fields: ['Item', 'Qty', 'Price', 'GST', 'Amount'], accent: '#0ea5e9' },
                { id: 'p9', name: 'Pharmacy Clean Invoice', desc: 'White + teal trust style', badge: 'Medical', badgeColor: '#0d9488', fields: ['Description', 'Quantity', 'Unit Price', 'Tax', 'Total'], accent: '#0d9488' },
                { id: 'p10', name: 'Furniture Premium Catalog', desc: 'Spacious luxury layout', badge: 'Clean', badgeColor: '#8b5cf6', fields: ['Item Description', 'Qty', 'Price', 'GST', 'Amount'], accent: '#8b5cf6' }
            ],
            service: [
                { id: 's1', name: 'Freelancer Invoice', desc: 'Split dark layout — developers & designers', badge: 'Popular', badgeColor: '#5b3fff', fields: ['Service', 'Hours', 'Rate', 'Total'], accent: '#5b3fff' },
                { id: 's2', name: 'Agency Invoice', desc: 'Blue dark header with contact bar', badge: 'New', badgeColor: '#0284c7', fields: ['Service', 'Hours', 'Rate', 'Total'], accent: '#0284c7' },
                { id: 's3', name: 'Consulting Invoice', desc: 'Elegant serif — management consultants', badge: null, badgeColor: null, fields: ['Service', 'Duration', 'Rate', 'Total'], accent: '#334155' },
                { id: 's4', name: 'Project Invoice', desc: 'Purple milestones with status column', badge: 'Trending', badgeColor: '#7c3aed', fields: ['Milestone', 'Hours', 'Rate', 'Status'], accent: '#7c3aed' },
                { id: 's5', name: 'Creative Service Invoice', desc: 'Dark rose — photographers & editors', badge: null, badgeColor: null, fields: ['Service', 'Hours', 'Rate', 'Total'], accent: '#db2777' },
                { id: 's6', name: 'Freelancer Creative', desc: 'Modern creative agency style', badge: 'Gradient', badgeColor: '#ec4899', fields: ['Creative Service', 'Hours', 'Rate', 'Total'], accent: '#ec4899' },
                { id: 's7', name: 'Consultant Executive', desc: 'Corporate navy clean layout', badge: 'Corp', badgeColor: '#1e3a8a', fields: ['Consulting Service', 'Hours', 'Rate/hr', 'Total'], accent: '#1e3a8a' },
                { id: 's8', name: 'Salon & Beauty Invoice', desc: 'Soft pink elegant design', badge: 'Beauty', badgeColor: '#f472b6', fields: ['Service Details', 'Hours', 'Rate', 'Amount'], accent: '#f472b6' },
                { id: 's9', name: 'Repair Service Work Order', desc: 'Technical structured layout', badge: 'Utility', badgeColor: '#f59e0b', fields: ['Task / Service', 'Hours', 'Rate', 'Total'], accent: '#f59e0b' },
                { id: 's10', name: 'Marketing Agency Premium', desc: 'Bold modern startup style', badge: 'Bold', badgeColor: '#ef4444', fields: ['Agency Service', 'Hours', 'Rate', 'Amount'], accent: '#ef4444' }
            ],
            subscription: [
                { id: 'sub1', name: 'Membership Invoice', desc: 'Green card layout for clubs & gyms', badge: 'Popular', badgeColor: '#4f46e5', fields: ['Plan', 'Duration', 'Price', 'Total'], accent: '#4f46e5' },
                { id: 'sub2', name: 'Gym Invoice', desc: 'Bold red fitness with member card block', badge: null, badgeColor: null, fields: ['Package', 'Duration', 'Price', 'Total'], accent: '#dc2626' },
                { id: 'sub3', name: 'Coaching Invoice', desc: 'Warm amber — coaching institutes', badge: 'New', badgeColor: '#d97706', fields: ['Course', 'Duration', 'Fee', 'Total'], accent: '#d97706' },
                { id: 'sub4', name: 'SaaS Billing Invoice', desc: 'Tech dark header for software subscriptions', badge: 'Tech', badgeColor: '#2563eb', fields: ['Plan', 'Seats', 'Cycle', 'Total'], accent: '#2563eb' },
                { id: 'sub5', name: 'Recurring Payment Invoice', desc: 'Indigo gradient — any recurring service', badge: null, badgeColor: null, fields: ['Service', 'Frequency', 'Price', 'Total'], accent: '#4f46e5' },
                { id: 'sub6', name: 'SaaS Monthly Billing', desc: 'Clean dashboard style', badge: 'SaaS', badgeColor: '#3b82f6', fields: ['SaaS Plan', 'Cycle', 'Fee', 'Total'], accent: '#3b82f6' },
                { id: 'sub7', name: 'Gym Membership Invoice', desc: 'Fitness energetic style', badge: 'Fitness', badgeColor: '#10b981', fields: ['Membership Plan', 'Duration', 'Rate', 'Amount'], accent: '#10b981' },
                { id: 'sub8', name: 'OTT / Streaming Bill', desc: 'Dark entertainment style', badge: 'Media', badgeColor: '#8b5cf6', fields: ['Subscription', 'Billing Cycle', 'Price', 'Total'], accent: '#8b5cf6' },
                { id: 'sub9', name: 'Tuition / Coaching Monthly', desc: 'Academic clean style', badge: 'Edu', badgeColor: '#0f766e', fields: ['Course / Details', 'Duration', 'Fee', 'Amount'], accent: '#0f766e' },
                { id: 'sub10', name: 'Internet / Utility Recurring', desc: 'Utility statement style', badge: 'Utility', badgeColor: '#64748b', fields: ['Plan Description', 'Billing Period', 'Charge', 'Total'], accent: '#64748b' }
            ]
        };"""

    # regex to replace TEMPLATES block
    regex = r"var TEMPLATES = \{[\s\S]*?\n        \};"
    
    files = ["templates.html", "builder.html"]
    for file in files:
        with open(file, "r") as f:
            content = f.read()
        
        content = re.sub(regex, templates_str, content)
        
        with open(file, "w") as f:
            f.write(content)
            
    print("HTML files updated")

if __name__ == "__main__":
    main()
