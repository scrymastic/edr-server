
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from utils.rule_item import RuleItem
from utils.rule_engine import RuleEngine
from utils.errors import error_to_json, ERROR_FAILED, ERROR_SUCCESS


def view_rules(request):
    rules = RuleItem.objects.all().order_by('-modified')
    rules_list = [
        {
            'id': rule.id,
            'title': rule.title,
            'status': rule.status,
            'level': rule.level,
            'is_active': rule.is_active,
        }
        for rule in rules
    ]
    rules_per_page = 200
    paginator = Paginator(rules_list, rules_per_page)
    page_number = request.GET.get('page', 1)
    rules = paginator.get_page(page_number)
    return render(request, 'rules/view_rules.html', {'item_page': rules})
    
    
def view_rule(request, rule_id):
    # Load a specific rule from the database
    rule_yaml = RuleItem.objects.get(id=rule_id).to_yaml()
    return render(request, 'rules/view_rule.html', {'rule_id': rule_id, 'yaml_content': rule_yaml})


def search_rules(request):
    query = request.POST.get('query')
    rules = RuleItem.search_rules(query)
    if rules:
        rules = rules.order_by('-modified')
        rules_list = [
            {
                'id': rule.id,
                'title': rule.title,
                'status': rule.status,
                'level': rule.level,
                'is_active': rule.is_active,
            }
            for rule in rules
        ]
    else:
        rules_list = []
    rules_per_page = 200
    paginator = Paginator(rules_list, rules_per_page)
    page_number = request.POST.get('page')
    item_page = paginator.get_page(page_number)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('rules/sample_table.html', {'item_page': item_page})
        return HttpResponse(html)
    else:
        return render(request, 'rules/view_rules.html', {'item_page': item_page})

def copy_rule(request, rule_id):
    rule_yaml = RuleItem.objects.get(id=rule_id).to_sample_yaml()
    return render(request, 'rules/create_rule.html', {'yaml_content': rule_yaml})


def toggle_rule(request):
    rule_id = request.POST.get('rule_id')
    is_active = request.POST.get('is_active')
    rule = RuleItem.objects.get(id=rule_id)
    if is_active == 'false' and rule.is_active:
        error_code = RuleEngine.undeploy_rule(rule_id)
        return JsonResponse(error_to_json(error_code))
    elif is_active == 'true' and not rule.is_active:
        error_code = RuleEngine.deploy_rule(rule_id)
        return JsonResponse(error_to_json(error_code))
    else:
        return JsonResponse(error_to_json(ERROR_FAILED))


def update_rule(request):
    rule_id = request.POST.get('rule_id')
    yaml = request.POST.get('yaml')
    rule = RuleItem.from_yaml(yaml)
    rule = rule.to_dict()
    if not rule:
        return JsonResponse(error_to_json(ERROR_FAILED))
    error_code = RuleEngine.update_rule(rule_id, rule)
    return JsonResponse(error_to_json(error_code))


def add_rule(request):
    rule = request.POST.get('yaml')
    rule = RuleItem.from_yaml(rule)
    rule.id = RuleItem.generate_id()
    rule.is_active = False
    rule = rule.to_dict()
    error_code = RuleEngine.add_rule(rule)
    return JsonResponse(error_to_json(error_code))


def delete_rule(request):
    rule_id = request.POST.get('rule_id')
    error_code = RuleEngine.remove_rule(rule_id)
    return JsonResponse(error_to_json(error_code))
    


