from talon.ui import Rect
from talon import ui
from concurrent.futures import ThreadPoolExecutor, as_completed

def is_clickable(element, depth=0):
    clickable = False

    try:
        control_type = element.control_type
    except:
        return clickable

    match control_type:
        case "Button":
            clickable = True
        case "ComboBox":
            clickable = True
        case "CheckBox":
            clickable = True
        case "Edit":
            clickable = True
        case "TreeItem":
            clickable = True   
        case "TabItem":
            clickable = True  
        case "SplitButton":
            clickable = True 
        case "ListViewItem":
            clickable = True      
        case "ListItem":   
            clickable = True 
        case "Menu":
            clickable = True        
        case "MenuItem":
            clickable = True    
        case _:
            clickable = element.is_keyboard_focusable
            # if not clickable:
            #     try:
            #         pattern = element.invoke_pattern
            #     except:
            #         pattern = None
            #         clickable = False

            #     if pattern and not isinstance(pattern, str):
            #         clickable = True
    # back up. todo: re-evaluate if this is necessary

                
    return clickable

def find_all_clickable_rects_parallel(element, filter_children=None, max_workers=8):
    # Do a shallow expansion on the main thread to avoid sending huge work units

    result = []
    # include root on main thread
    try:
        if element.is_enabled and not element.is_offscreen and is_clickable(element):
            result.append(element.rect)
    except Exception:
        pass

    try:
        children = element.children
    except Exception:
        children = []

    def worker(subroot, filter_children):
        # WARNING: only safe if subroot is safe to access in worker threads
        if filter_children:
            if subroot.control_type in filter_children:
                if subroot.name in filter_children[subroot.control_type]:

                    return find_all_clickable_rects_parallel(subroot)
                
                #print(f"{subroot.name}: {subroot.control_type}")
                return []
        else:
            return find_all_clickable_rects_parallel(subroot)
        
    if len(children) > 0:
        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            futures = [ex.submit(worker, ch, filter_children) for ch in children]
            for f in as_completed(futures):
                try:
                    result.extend(f.result())
                except Exception:
                    pass

    return result

def find_all_clickable_elements_parallel(element, max_workers=8):
    # Do a shallow expansion on the main thread to avoid sending huge work units

    result = []
    # include root on main thread
    try:
        if element.is_enabled and not element.is_offscreen and is_clickable(element):
            result.append(element)
    except Exception:
        pass

    try:
        children = element.children
    except Exception:
        children = []

    def worker(subroot):
        # WARNING: only safe if subroot is safe to access in worker threads
        return find_all_clickable_elements_parallel(subroot)

    if len(children) > 0:
        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            futures = [ex.submit(worker, ch) for ch in children]
            for f in as_completed(futures):
                try:
                    result.extend(f.result())
                except Exception:
                    pass

    return result

def find_all_clickable_rects(element, depth=0) -> list[Rect]:
    result = []
    name = element.name
    control_type = element.control_type

    if (is_clickable(element)):
        result.append(element.rect)

        #print("  " * depth + f"{element.control_type}: {element.name}")
    #else:
        #print("  " * depth + f"*{element.control_type}: {element.name}")

    # match control_type:
    #     case "Pane":
    #         selection_item_pattern = element.selectionitem_pattern
    #         if not selection_item_pattern.is_selected:
    #             print("tab not selected!!")
    #             return result

    try:
        children = element.children
    except Exception as e:
        #print(f"all clickable exception {e} {name}")
        return result 

    for child in children:
        child_result = find_all_clickable_rects(child, depth + 1)
        result.extend(child_result)

    return result

def process_children_in_parallel(targets):
    results = []
    # First pass: select which children to process (serial, deterministic)
    # Parallel execution using threads
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(find_all_clickable_rects_parallel, child)
            for child in targets
        ]

        for future in as_completed(futures):
            try:
                result = future.result()
                if result:
                    results.extend(result)
            except Exception as exc:
                # handle/log per-task failures without killing the whole run
                print(f"Thread failed: {exc}")

    return results

def find_all_clickable_elements(element, depth=0) -> list:
    result = []
    
    if (not element.is_offscreen and is_clickable(element)):
        result.append(element)

    # if the element is disabled, can we safely skip?
    try:
        children = element.children
    except Exception as e:
        
        #print(f"all clickable exception {e} {name}")
        return result 

    for child in children:
        child_result = find_all_clickable_elements(child, depth + 1)
        result.extend(child_result)

    return result


def walk(element, depth=0):
    if element.automation_id:
        print("  " * depth + f"{element.control_type}: {element.name}, automation_id = {element.automation_id}") 
    
    try:
        for child in element.children:
            walk(child, depth + 1)
    except (OSError, RuntimeError):
        pass  # Element became stale

def on_title_change(_):
    print(ui.active_window().title)

def on_focus_change(_):
    window = ui.active_window()
    print(f"window focus: {ui.focused_element().name} {window.cls} {window.id}")

def on_focused_element_change(_):
    window = ui.active_window()
    print(f"element focus: {ui.focused_element().name} {window.cls} {window.id}")
    
ui.register("win_focus", on_focus_change)
#ui.register("win_title", on_title_change)
ui.register("element_focus", on_focused_element_change)
