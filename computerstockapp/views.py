from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse
from .models import ComputerStock
import csv
import io
from decimal import Decimal, InvalidOperation

def computer_list(request):
    # Show only non-archived computers by default
    show_archived = request.GET.get('show_archived', False)
    if show_archived:
        computers = ComputerStock.objects.all()
    else:
        computers = ComputerStock.objects.filter(is_archived=False)
    
    context = {
        'computers': computers,
        'show_archived': show_archived
    }
    return render(request, 'computerstockapp/computer_list.html', context)

def add_computer(request):
    if request.method == 'POST':
        computer_name = request.POST.get('computer_name')
        brand = request.POST.get('brand')
        model = request.POST.get('model')
        processor = request.POST.get('processor')
        ram = request.POST.get('ram')
        storage = request.POST.get('storage')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        
        computer = ComputerStock.objects.create(
            computer_name=computer_name,
            brand=brand,
            model=model,
            processor=processor,
            ram=ram,
            storage=storage,
            price=price,
            quantity=quantity
        )
        messages.success(request, 'Computer added successfully!')
        return redirect('computer_list')
    
    return render(request, 'computerstockapp/add_computer.html')

def edit_computer(request, computer_id):
    computer = get_object_or_404(ComputerStock, id=computer_id)
    
    if request.method == 'POST':
        computer.computer_name = request.POST.get('computer_name')
        computer.brand = request.POST.get('brand')
        computer.model = request.POST.get('model')
        computer.processor = request.POST.get('processor')
        computer.ram = request.POST.get('ram')
        computer.storage = request.POST.get('storage')
        computer.price = request.POST.get('price')
        computer.quantity = request.POST.get('quantity')
        computer.save()
        
        messages.success(request, 'Computer updated successfully!')
        return redirect('computer_list')
    
    return render(request, 'computerstockapp/edit_computer.html', {'computer': computer})

def delete_computer(request, computer_id):
    computer = get_object_or_404(ComputerStock, id=computer_id)
    
    if request.method == 'POST':
        delete_type = request.POST.get('delete_type')
        
        if delete_type == 'soft':
            # Soft delete - archive the computer
            computer.is_archived = True
            computer.save()
            messages.success(request, f'Computer "{computer.computer_name}" has been archived successfully!')
        elif delete_type == 'hard':
            # Hard delete - permanently remove from database
            computer_name = computer.computer_name
            computer.delete()
            messages.success(request, f'Computer "{computer_name}" has been permanently deleted!')
        
        return redirect('computer_list')
    
    return render(request, 'computerstockapp/delete_computer.html', {'computer': computer})

def restore_computer(request, computer_id):
    """Restore an archived computer"""
    computer = get_object_or_404(ComputerStock, id=computer_id, is_archived=True)
    
    if request.method == 'POST':
        computer.is_archived = False
        computer.save()
        messages.success(request, f'Computer "{computer.computer_name}" has been restored successfully!')
        return redirect('computer_list')
    
    return render(request, 'computerstockapp/restore_computer.html', {'computer': computer})

def archived_computers(request):
    """Show only archived computers"""
    computers = ComputerStock.objects.filter(is_archived=True)
    return render(request, 'computerstockapp/archived_computers.html', {'computers': computers})

def export_csv(request):
    """Export all computers to CSV file"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="computer_inventory.csv"'
    
    writer = csv.writer(response)
      # Write CSV header
    writer.writerow([
        'Computer Name', 'Brand', 'Model', 'Processor', 'RAM', 
        'Storage', 'Price', 'Quantity', 'Is Archived', 'Date Added', 'Date Modified'
    ])
    
    # Write data rows (export all computers including archived ones)
    computers = ComputerStock.objects.all()
    for computer in computers:
        writer.writerow([
            computer.computer_name,
            computer.brand,
            computer.model,
            computer.processor,
            computer.ram,
            computer.storage,
            str(computer.price),
            computer.quantity,
            'Yes' if computer.is_archived else 'No',
            computer.date_added.strftime('%Y-%m-%d %H:%M:%S'),
            computer.date_modified.strftime('%Y-%m-%d %H:%M:%S')
        ])
    
    return response

def import_csv(request):
    """Import computers from CSV file"""
    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file')
        
        if not csv_file:
            messages.error(request, 'Please select a CSV file to upload.')
            return render(request, 'computerstockapp/import_csv.html')
        
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a valid CSV file.')
            return render(request, 'computerstockapp/import_csv.html')
        
        try:
            # Read CSV file
            decoded_file = csv_file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            reader = csv.reader(io_string)
            
            # Skip header row
            header = next(reader, None)
            if not header:
                messages.error(request, 'CSV file appears to be empty.')
                return render(request, 'computerstockapp/import_csv.html')
              # Expected header format (core required fields)
            expected_headers = [
                'Computer Name', 'Brand', 'Model', 'Processor', 'RAM', 
                'Storage', 'Price', 'Quantity'
            ]
            
            # Check if we have the optional Is Archived column
            has_archived_column = len(header) > 8 and header[8] == 'Is Archived'
            
            # Validate headers (check first 8 columns)
            if len(header) < 8 or header[:8] != expected_headers:
                expected_with_optional = expected_headers + ['Is Archived (optional)']
                messages.error(request, f'CSV header format is incorrect. Expected: {", ".join(expected_with_optional)}')
                return render(request, 'computerstockapp/import_csv.html')
            
            imported_count = 0
            error_rows = []
            
            for row_num, row in enumerate(reader, start=2):  # Start from row 2 (after header)
                if len(row) < 8:
                    error_rows.append(f'Row {row_num}: Insufficient columns')
                    continue
                
                try:
                    # Validate and convert data
                    computer_name = row[0].strip()
                    brand = row[1].strip()
                    model = row[2].strip()
                    processor = row[3].strip()
                    ram = row[4].strip()
                    storage = row[5].strip()
                    
                    # Validate price
                    try:
                        price = Decimal(row[6].strip())
                        if price < 0:
                            raise ValueError("Price cannot be negative")
                    except (ValueError, InvalidOperation):
                        error_rows.append(f'Row {row_num}: Invalid price value "{row[6]}"')
                        continue
                      # Validate quantity
                    try:
                        quantity = int(row[7].strip())
                        if quantity < 0:
                            raise ValueError("Quantity cannot be negative")
                    except ValueError:
                        error_rows.append(f'Row {row_num}: Invalid quantity value "{row[7]}"')
                        continue
                    
                    # Handle is_archived field (optional)
                    is_archived = False
                    if has_archived_column and len(row) > 8:
                        archived_value = row[8].strip().lower()
                        if archived_value in ['yes', 'true', '1']:
                            is_archived = True
                        elif archived_value in ['no', 'false', '0', '']:
                            is_archived = False
                        else:
                            error_rows.append(f'Row {row_num}: Invalid archived value "{row[8]}". Use "Yes" or "No"')
                            continue
                    
                    # Check for required fields
                    if not all([computer_name, brand, model]):
                        error_rows.append(f'Row {row_num}: Computer name, brand, and model are required')
                        continue
                      # Create computer record
                    ComputerStock.objects.create(
                        computer_name=computer_name,
                        brand=brand,
                        model=model,
                        processor=processor,
                        ram=ram,
                        storage=storage,
                        price=price,
                        quantity=quantity,
                        is_archived=is_archived
                    )
                    imported_count += 1
                    
                except Exception as e:
                    error_rows.append(f'Row {row_num}: {str(e)}')
            
            # Show results
            if imported_count > 0:
                messages.success(request, f'Successfully imported {imported_count} computer(s).')
            
            if error_rows:
                error_message = f'Errors encountered in {len(error_rows)} row(s):\n' + '\n'.join(error_rows[:10])
                if len(error_rows) > 10:
                    error_message += f'\n... and {len(error_rows) - 10} more errors.'
                messages.warning(request, error_message)
            
            if imported_count == 0 and not error_rows:
                messages.info(request, 'No data was imported from the CSV file.')
            
            return redirect('computer_list')
            
        except Exception as e:
            messages.error(request, f'Error processing CSV file: {str(e)}')
    
    return render(request, 'computerstockapp/import_csv.html')
