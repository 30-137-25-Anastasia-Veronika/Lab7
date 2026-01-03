adjacency_list = {
    1: None,
    2: 1,
    3: 1,
    4: 2,
    5: 2,
    6: 3,
    7: 3,
    8: 4,
    9: 6
}

node_names = {
    1: "Root", 2: "A", 3: "B", 4: "A1", 5: "A2",
    6: "B1", 7: "B2", 8: "A1a", 9: "B1a"
}


def show_adjacency_tree(adj_list, names):
    """Показываем дерево из Adjacency List"""
    print("=== Дерево (Adjacency List) ===")
    roots = [n for n, p in adj_list.items() if p is None]
    for root in roots:
        show_subtree(root, adj_list, names, 0)


def show_subtree(node_id, adj_list, names, level):
    """Рекурсивно показываем поддерево"""
    indent = "  " * level
    name = names.get(node_id, "")
    print(f"{indent}{node_id} ({name})" if name else f"{indent}{node_id}")

    children = [c for c, p in adj_list.items() if p == node_id]
    for child in sorted(children):
        show_subtree(child, adj_list, names, level + 1)



def adjacency_to_nested(adj_list):
    """Конвертируем Adjacency List → Nested Sets"""
    nested = {}
    counter = 1

    def dfs(node_id):
        nonlocal counter
        left = counter
        counter += 1

        children = [c for c, p in adj_list.items() if p == node_id]
        for child in children:
            dfs(child)

        right = counter
        counter += 1
        nested[node_id] = (left, right)

    roots = [n for n, p in adj_list.items() if p is None]
    for root in roots:
        dfs(root)

    return nested

def nested_to_adjacency(nested):
    """Конвертируем Nested Sets → Adjacency List"""
    adjacency = {}
    sorted_nodes = sorted(nested.items(), key=lambda x: x[1][0])
    stack = []

    for node_id, (left, right) in sorted_nodes:
        parent_id = None
        for i in range(len(stack) - 1, -1, -1):
            parent_node, parent_left, parent_right = stack[i]
            if parent_left < left and parent_right > right:
                parent_id = parent_node
                break

        adjacency[node_id] = parent_id

        while stack and stack[-1][2] < left:
            stack.pop()

        stack.append((node_id, left, right))

    return adjacency


def main():
    show_adjacency_tree(adjacency_list, node_names)

    # Конвертируем в Nested Sets
    print("\n" + "=" * 50)
    print("Конвертация Adjacency List → Nested Sets")
    print("=" * 50)

    nested_sets = adjacency_to_nested(adjacency_list)

    for node_id in sorted(nested_sets.keys()):
        left, right = nested_sets[node_id]
        name = node_names.get(node_id, "")
        print(f"Узел {node_id} ({name}): left={left}, right={right}")

    print("\n" + "=" * 50)
    print("Конвертация Nested Sets → Adjacency List")
    print("=" * 50)

    converted = nested_to_adjacency(nested_sets)

    print("Исходный Adjacency List:")
    for node_id in sorted(adjacency_list.keys()):
        print(f"  {node_id}: {adjacency_list[node_id]}")

    print("\nВосстановленный Adjacency List:")
    for node_id in sorted(converted.keys()):
        print(f"  {node_id}: {converted[node_id]}")

    if adjacency_list == converted:
        print("\n✓ Конвертация работает корректно!")
    else:
        print("\n✗ Ошибка в конвертации")


if __name__ == "__main__":
    main()