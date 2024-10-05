import tkinter as tk
from tkinter import ttk, messagebox, font
from graphviz import Digraph
import os

class FamilyMember:
    def __init__(self, name):
        self.name = name
        self.relations = {}

class FamilyTree:
    def __init__(self):
        self.members = {}

    def add_member(self, name):
        if name not in self.members:
            self.members[name] = FamilyMember(name)
            return True
        return False

    def add_relation(self, name1, name2, relation):
        if name1 in self.members and name2 in self.members:
            self.members[name1].relations[name2] = relation
            if relation in ["配偶", "Spouse"]:
                self.members[name2].relations[name1] = relation
            elif relation in ["父親", "Father", "母親", "Mother"]:
                self.members[name2].relations[name1] = "子女" if self.lang == "zh" else "Child"
            elif relation in ["子女", "Child"]:
                if "Gender" in self.members[name1].relations:
                    if self.members[name1].relations["Gender"] == "Male":
                        self.members[name2].relations[name1] = "父親" if self.lang == "zh" else "Father"
                    else:
                        self.members[name2].relations[name1] = "母親" if self.lang == "zh" else "Mother"
            return True
        return False

    def set_gender(self, name, gender):
        if name in self.members:
              # 存儲性別時使用統一的鍵 "Gender"
            self.members[name].relations["Gender"] = gender
            return True
        return False

class FamilyTreeGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("家族樹建立程式")
        self.master.geometry("700x550")  # 調整主窗口大小
        self.family_tree = FamilyTree()
        self.lang = "zh"  # 預設語言為中文

        # 設置字體
        self.default_font = font.nametofont("TkDefaultFont")
        self.default_font.configure(size=12)
        self.large_font = font.Font(size=14)

        self.translations = {
            "zh": {
                "title": "家族樹建立程式",
                "member_name": "成員姓名:",
                "add_member": "添加成員",
                "gender": "性別:",
                "set_gender": "設置性別",
                "member1": "成員1:",
                "relation": "關係:",
                "member2": "成員2:",
                "add_relation": "添加關係",
                "display_tree": "顯示家族樹",
                "male": "男",
                "female": "女",
                "spouse": "配偶",
                "father": "父親",
                "mother": "母親",
                "child": "子女",
                "brother": "兄弟",
                "sister": "姐妹",
                "success": "成功",
                "error": "錯誤",
                "member_added": "已添加成員: {}",
                "member_exists": "成員 {} 已存在",
                "enter_name": "請輸入姓名",
                "gender_set": "已設置 {} 的性別為 {}",
                "cant_set_gender": "無法設置性別",
                "select_member_gender": "請選擇成員和性別",
                "relation_added": "已添加關係: {} 是 {} 的 {}",
                "cant_add_relation": "無法添加關係",
                "select_members_relation": "請選擇成員和關係",
                "family_tree": "家族樹:",
                "unknown": "未知",
                "graphviz_error": "無法生成圖形版本的家族樹。錯誤信息：{}\n\n請確保已正確安裝 Graphviz 並將其添加到系統 PATH 中。",
                "switch_to_en": "Switch to English"
            },
            "en": {
                "title": "Family Tree Builder",
                "member_name": "Member Name:",
                "add_member": "Add Member",
                "gender": "Gender:",
                "set_gender": "Set Gender",
                "member1": "Member 1:",
                "relation": "Relation:",
                "member2": "Member 2:",
                "add_relation": "Add Relation",
                "display_tree": "Display Family Tree",
                "male": "Male",
                "female": "Female",
                "spouse": "Spouse",
                "father": "Father",
                "mother": "Mother",
                "child": "Child",
                "brother": "Brother",
                "sister": "Sister",
                "success": "Success",
                "error": "Error",
                "member_added": "Member added: {}",
                "member_exists": "Member {} already exists",
                "enter_name": "Please enter a name",
                "gender_set": "Set {}'s gender to {}",
                "cant_set_gender": "Unable to set gender",
                "select_member_gender": "Please select a member and gender",
                "relation_added": "Relation added: {} is {}'s {}",
                "cant_add_relation": "Unable to add relation",
                "select_members_relation": "Please select members and relation",
                "family_tree": "Family Tree:",
                "unknown": "Unknown",
                "graphviz_error": "Unable to generate graphical version of the family tree. Error message: {}\n\nPlease ensure Graphviz is correctly installed and added to the system PATH.",
                "switch_to_zh": "切換到中文"
            }
        }

        self.create_widgets()

    def create_widgets(self):
        self.master.grid_columnconfigure(1, weight=1)

        # 語言切換按鈕
        self.lang_button = tk.Button(self.master, text=self.translations[self.lang]["switch_to_en"], command=self.switch_language, font=self.large_font)
        self.lang_button.grid(row=0, column=2, padx=10, pady=10, sticky="e")

        # 添加成員
        self.name_label = tk.Label(self.master, text=self.translations[self.lang]["member_name"], font=self.large_font)
        self.name_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.name_entry = tk.Entry(self.master, font=self.large_font, width=20)
        self.name_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.add_button = tk.Button(self.master, text=self.translations[self.lang]["add_member"], command=self.add_member, font=self.large_font)
        self.add_button.grid(row=1, column=2, padx=10, pady=10)

        # 設置性別
        self.gender_label = tk.Label(self.master, text=self.translations[self.lang]["gender"], font=self.large_font)
        self.gender_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.gender_combo = ttk.Combobox(self.master, values=[self.translations[self.lang]["male"], self.translations[self.lang]["female"]], font=self.large_font, width=18)
        self.gender_combo.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        self.set_gender_button = tk.Button(self.master, text=self.translations[self.lang]["set_gender"], command=self.set_gender, font=self.large_font)
        self.set_gender_button.grid(row=2, column=2, padx=10, pady=10)

        # 添加關係
        self.member1_label = tk.Label(self.master, text=self.translations[self.lang]["member1"], font=self.large_font)
        self.member1_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.member1_combo = ttk.Combobox(self.master, font=self.large_font, width=18)
        self.member1_combo.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        self.relation_label = tk.Label(self.master, text=self.translations[self.lang]["relation"], font=self.large_font)
        self.relation_label.grid(row=4, column=0, padx=10, pady=10, sticky="e")
        self.relation_combo = ttk.Combobox(self.master, values=[self.translations[self.lang][rel] for rel in ["spouse", "father", "mother", "child", "brother", "sister"]], font=self.large_font, width=18)
        self.relation_combo.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

        self.member2_label = tk.Label(self.master, text=self.translations[self.lang]["member2"], font=self.large_font)
        self.member2_label.grid(row=5, column=0, padx=10, pady=10, sticky="e")
        self.member2_combo = ttk.Combobox(self.master, font=self.large_font, width=18)
        self.member2_combo.grid(row=5, column=1, padx=10, pady=10, sticky="ew")

        self.add_relation_button = tk.Button(self.master, text=self.translations[self.lang]["add_relation"], command=self.add_relation, font=self.large_font)
        self.add_relation_button.grid(row=6, column=1, padx=10, pady=10)

        # 顯示家族樹
        self.display_button = tk.Button(self.master, text=self.translations[self.lang]["display_tree"], command=self.display_family_tree, font=self.large_font)
        self.display_button.grid(row=7, column=1, padx=10, pady=10)

    def switch_language(self):
        self.lang = "en" if self.lang == "zh" else "zh"
        self.update_ui_text()

    def update_ui_text(self):
        self.master.title(self.translations[self.lang]["title"])
        self.lang_button.config(text=self.translations[self.lang]["switch_to_en" if self.lang == "zh" else "switch_to_zh"])
        self.name_label.config(text=self.translations[self.lang]["member_name"])
        self.add_button.config(text=self.translations[self.lang]["add_member"])
        self.gender_label.config(text=self.translations[self.lang]["gender"])
        self.gender_combo.config(values=[self.translations[self.lang]["male"], self.translations[self.lang]["female"]])
        self.set_gender_button.config(text=self.translations[self.lang]["set_gender"])
        self.member1_label.config(text=self.translations[self.lang]["member1"])
        self.relation_label.config(text=self.translations[self.lang]["relation"])
        self.relation_combo.config(values=[self.translations[self.lang][rel] for rel in ["spouse", "father", "mother", "child", "brother", "sister"]])
        self.member2_label.config(text=self.translations[self.lang]["member2"])
        self.add_relation_button.config(text=self.translations[self.lang]["add_relation"])
        self.display_button.config(text=self.translations[self.lang]["display_tree"])

    def add_member(self):
        name = self.name_entry.get()
        if name:
            if self.family_tree.add_member(name):
                messagebox.showinfo(self.translations[self.lang]["success"], self.translations[self.lang]["member_added"].format(name))
                self.update_member_combos()
            else:
                messagebox.showerror(self.translations[self.lang]["error"], self.translations[self.lang]["member_exists"].format(name))
        else:
            messagebox.showerror(self.translations[self.lang]["error"], self.translations[self.lang]["enter_name"])

    def set_gender(self):
        name = self.member1_combo.get()
        gender = self.gender_combo.get()
        if name and gender:
            # 將用戶界面的性別選擇轉換為英文存儲
            gender_en = "Male" if gender == self.translations[self.lang]["male"] else "Female"
            if self.family_tree.set_gender(name, gender_en):
                messagebox.showinfo(self.translations[self.lang]["success"], self.translations[self.lang]["gender_set"].format(name, gender))
            else:
                messagebox.showerror(self.translations[self.lang]["error"], self.translations[self.lang]["cant_set_gender"])
        else:
            messagebox.showerror(self.translations[self.lang]["error"], self.translations[self.lang]["select_member_gender"])


    def add_relation(self):
        member1 = self.member1_combo.get()
        member2 = self.member2_combo.get()
        relation = self.relation_combo.get()
        if member1 and member2 and relation:
            if self.family_tree.add_relation(member1, member2, relation):
                messagebox.showinfo(self.translations[self.lang]["success"], self.translations[self.lang]["relation_added"].format(member1, member2, relation))
            else:
                messagebox.showerror(self.translations[self.lang]["error"], self.translations[self.lang]["cant_add_relation"])
        else:
            messagebox.showerror(self.translations[self.lang]["error"], self.translations[self.lang]["select_members_relation"])

    def update_member_combos(self):
        members = list(self.family_tree.members.keys())
        self.member1_combo['values'] = members
        self.member2_combo['values'] = members

    def display_family_tree(self):
            tree_str = self.translations[self.lang]["family_tree"] + "\n"
            for member, data in self.family_tree.members.items():
                tree_str += f"{member}"
                if "Gender" in data.relations:
                    gender_display = self.translations[self.lang]["male"] if data.relations["Gender"] == "Male" else self.translations[self.lang]["female"]
                    tree_str += f" ({gender_display})"
                tree_str += ":\n"
                for relative, relation in data.relations.items():
                    if relative != "Gender":
                        tree_str += f"  - {relative} ({relation})\n"
            
            # 顯示文本版本的家族樹
            self.show_large_text_dialog(self.translations[self.lang]["family_tree"], tree_str)

            try:
                # 创建图形
                dot = Digraph(comment='Family Tree', format='png')
                dot.attr(rankdir='TB', charset='UTF-8')
                dot.attr('node', fontname='SimSun' if self.lang == 'zh' else 'Arial', fontsize='20')

                # 用于存储已处理的关系和父母对
                processed_relations = set()
                parent_pairs = {}
                children = {}
                
                # 第一遍：添加所有节点和识别关系
                for member, data in self.family_tree.members.items():
                    gender = data.relations.get("Gender", "Unknown")
                    gender_display = self.translations[self.lang]["male"] if gender == "Male" else self.translations[self.lang]["female"] if gender == "Female" else self.translations[self.lang]["unknown"]
                    color = "lightblue" if gender == "Male" else "pink" if gender == "Female" else "lightgrey"
                    label = f'<<TABLE BORDER="0" CELLBORDER="0"><TR><TD>{member}</TD></TR><TR><TD>({gender_display})</TD></TR></TABLE>>'
                    dot.node(member, label, style="filled", fillcolor=color, shape='circle', width='1.5', height='1.5')

                    for relative, relation in data.relations.items():
                        if relation in [self.translations[self.lang]["spouse"], "配偶"]:
                            if (member, relative) not in processed_relations and (relative, member) not in processed_relations:
                                parent_pair_id = f"{member}_{relative}_pair"
                                parent_pairs[frozenset([member, relative])] = parent_pair_id
                                processed_relations.add((member, relative))
                        elif relation in [self.translations[self.lang]["child"], "子女"]:
                            if member not in children:
                                children[member] = []
                            children[member].append(relative)
                        elif relation in [self.translations[self.lang]["father"], self.translations[self.lang]["mother"], "父親", "母親"]:
                            if relative not in children:
                                children[relative] = []
                            children[relative].append(member)

                # 第二遍：添加关系
                for pair, pair_id in parent_pairs.items():
                    parents = list(pair)
                    dot.node(pair_id, "", shape="point", width="0.1")
                    with dot.subgraph() as s:
                        s.attr(rank='same')
                        s.edge(parents[0], pair_id, style="invis")
                        s.edge(pair_id, parents[1], style="invis")
                    dot.edge(parents[0], parents[1], dir="none", color="red")

                    # 添加父母到子女的箭头
                    for parent in parents:
                        if parent in children:
                            for child in children[parent]:
                                dot.edge(pair_id, child, dir="forward", arrowhead="normal")

                # 处理单亲情况
                for parent, parent_children in children.items():
                    if not any(parent in pair for pair in parent_pairs):
                        for child in parent_children:
                            dot.edge(parent, child, dir="forward", arrowhead="normal")

                # 保存并显示图形
                dot.render("family_tree", view=True, cleanup=True)
            except Exception as e:
                error_message = self.translations[self.lang]["graphviz_error"].format(str(e))
                messagebox.showerror(self.translations[self.lang]["error"], error_message)
                print(error_message)  # 在控制台也输出错误信息

    def show_large_text_dialog(self, title, text):
        dialog = tk.Toplevel(self.master)
        dialog.title(title)
        dialog.geometry("600x400")

        text_widget = tk.Text(dialog, wrap=tk.WORD, font=self.large_font)
        text_widget.pack(expand=True, fill=tk.BOTH)
        text_widget.insert(tk.END, text)
        text_widget.config(state=tk.DISABLED)

        scrollbar = tk.Scrollbar(dialog, command=text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.config(yscrollcommand=scrollbar.set)

        ok_button = tk.Button(dialog, text="OK", command=dialog.destroy)
        ok_button.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = FamilyTreeGUI(root)
    root.mainloop()