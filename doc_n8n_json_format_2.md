Based on the documentation retrieved from n8n's official sources, here's a comprehensive overview of JSON formats used in n8n:                                                                                                              


                                                                                                          n8n JSON Data Structure                                                                                                           

                                                                                                            Standard Data Format                                                                                                            

n8n uses a specific JSON structure for data passed between nodes:                                                                                                                                                                           

                                                                                                                                                                                                                                            
 [                                                                                                                                                                                                                                          
   {                                                                                                                                                                                                                                        
     "json": {                                                                                                                                                                                                                              
       "key1": "value1",                                                                                                                                                                                                                    
       "key2": {                                                                                                                                                                                                                            
         "nested": "data"                                                                                                                                                                                                                   
       }                                                                                                                                                                                                                                    
     },                                                                                                                                                                                                                                     
     "binary": {                                                                                                                                                                                                                            
       "file-name": {                                                                                                                                                                                                                       
         "data": "base64-encoded-data",                                                                                                                                                                                                     
         "mimeType": "image/png",                                                                                                                                                                                                           
         "fileExtension": "png",                                                                                                                                                                                                            
         "fileName": "example.png"                                                                                                                                                                                                          
       }                                                                                                                                                                                                                                    
     }                                                                                                                                                                                                                                      
   }                                                                                                                                                                                                                                        
 ]                                                                                                                                                                                                                                          
                                                                                                                                                                                                                                            

                                                                                                              Key Components:                                                                                                               

 • json: Contains the main data payload (required)                                                                                                                                                                                          
 • binary: Contains binary file data (optional)                                                                                                                                                                                             
 • pairedItem: Links output to specific input items (optional)                                                                                                                                                                              

                                                                                                            Webhook Data Format                                                                                                             

When receiving data via webhooks:                                                                                                                                                                                                           

                                                                                                                                                                                                                                            
 [                                                                                                                                                                                                                                          
   {                                                                                                                                                                                                                                        
     "headers": {                                                                                                                                                                                                                           
       "host": "n8n.instance.address"                                                                                                                                                                                                       
     },                                                                                                                                                                                                                                     
     "params": {},                                                                                                                                                                                                                          
     "query": {},                                                                                                                                                                                                                           
     "body": {                                                                                                                                                                                                                              
       "name": "Jim",                                                                                                                                                                                                                       
       "age": 30,                                                                                                                                                                                                                           
       "city": "New York"                                                                                                                                                                                                                   
     }                                                                                                                                                                                                                                      
   }                                                                                                                                                                                                                                        
 ]                                                                                                                                                                                                                                          
                                                                                                                                                                                                                                            

                                                                                                       Workflow Configuration Format                                                                                                        

n8n workflows are defined in JSON format:                                                                                                                                                                                                   

                                                                                                                                                                                                                                            
 {                                                                                                                                                                                                                                          
   "name": "My Workflow",                                                                                                                                                                                                                   
   "nodes": [                                                                                                                                                                                                                               
     {                                                                                                                                                                                                                                      
       "parameters": {},                                                                                                                                                                                                                    
       "name": "Start",                                                                                                                                                                                                                     
       "type": "n8n-nodes-base.start",                                                                                                                                                                                                      
       "id": "uuid-here"                                                                                                                                                                                                                    
     }                                                                                                                                                                                                                                      
   ],                                                                                                                                                                                                                                       
   "connections": {},                                                                                                                                                                                                                       
   "active": false,                                                                                                                                                                                                                         
   "settings": {},                                                                                                                                                                                                                          
   "tags": []                                                                                                                                                                                                                               
 }                                                                                                                                                                                                                                          
                                                                                                                                                                                                                                            

                                                                                                         Expression Format for JSON                                                                                                         

When using expressions in HTTP Request nodes:                                                                                                                                                                                               

                                                                                                                                                                                                                                            
 {{                                                                                                                                                                                                                                         
   {                                                                                                                                                                                                                                        
     "myjson": {                                                                                                                                                                                                                            
       "name1": "value1",                                                                                                                                                                                                                   
       "name2": "value2",                                                                                                                                                                                                                   
       "array1": ["value1", "value2"]                                                                                                                                                                                                       
     }                                                                                                                                                                                                                                      
   }                                                                                                                                                                                                                                        
 }}                                                                                                                                                                                                                                         
                                                                                                                                                                                                                                            

                                                                                                            Configuration Files                                                                                                             

n8n configuration files use JSON format:                                                                                                                                                                                                    

                                                                                                                                                                                                                                            
 {                                                                                                                                                                                                                                          
   "executions": {                                                                                                                                                                                                                          
     "saveDataOnSuccess": "none"                                                                                                                                                                                                            
   },                                                                                                                                                                                                                                       
   "generic": {                                                                                                                                                                                                                             
     "timezone": "Europe/Berlin"                                                                                                                                                                                                            
   },                                                                                                                                                                                                                                       
   "nodes": {                                                                                                                                                                                                                               
     "exclude": ["n8n-nodes-base.executeCommand"]                                                                                                                                                                                           
   },                                                                                                                                                                                                                                       
   "endpoints": {                                                                                                                                                                                                                           
     "metrics": {                                                                                                                                                                                                                           
       "enable": true                                                                                                                                                                                                                       
     }                                                                                                                                                                                                                                      
   }                                                                                                                                                                                                                                        
 }                                                                                                                                                                                                                                          
                                                                                                                                                                                                                                            

                                                                                                        Data Transformation Examples                                                                                                        

For transforming data within n8n:                                                                                                                                                                                                           

                                                                                                                                                                                                                                            
 {                                                                                                                                                                                                                                          
   "newKey": "new value",                                                                                                                                                                                                                   
   "array": [{{ $json.id }}, "{{ $json.name }}"],                                                                                                                                                                                           
   "object": {                                                                                                                                                                                                                              
     "innerKey1": "new value",                                                                                                                                                                                                              
     "innerKey2": "{{ $json.id }}",                                                                                                                                                                                                         
     "innerKey3": "{{ $json.name }}"                                                                                                                                                                                                        
   }                                                                                                                                                                                                                                        
 }                                                                                                                                                                                                                                          
                                                                                                                                                                                                                                            

                                                                                                          Form Field Configuration                                                                                                          

JSON for defining form fields:                                                                                                                                                                                                              

                                                                                                                                                                                                                                            
 [                                                                                                                                                                                                                                          
   {                                                                                                                                                                                                                                        
     "fieldLabel": "Email",                                                                                                                                                                                                                 
     "fieldType": "email",                                                                                                                                                                                                                  
     "placeholder": "me@mail.com"                                                                                                                                                                                                           
   },                                                                                                                                                                                                                                       
   {                                                                                                                                                                                                                                        
     "fieldLabel": "Dropdown Options",                                                                                                                                                                                                      
     "fieldType": "dropdown",                                                                                                                                                                                                               
     "fieldOptions": {                                                                                                                                                                                                                      
       "values": [                                                                                                                                                                                                                          
         {"option": "option 1"},                                                                                                                                                                                                            
         {"option": "option 2"}                                                                                                                                                                                                             
       ]                                                                                                                                                                                                                                    
     }                                                                                                                                                                                                                                      
   }                                                                                                                                                                                                                                        
 ]                                                                                                                                                                                                                                          
                                                                                                                                                                                                                                            

                                                                                                              JMESPath Queries                                                                                                              

n8n supports JMESPath for JSON querying:                                                                                                                                                                                                    

                                                                                                                                                                                                                                            
 // Extract first names from people array                                                                                                                                                                                                   
 {{$jmespath($json.body.people, "[*].first")}}                                                                                                                                                                                              
                                                                                                                                                                                                                                            
 // Filter and extract specific data                                                                                                                                                                                                        
 {{ $jmespath($("Code").all(), "[?json.name=='Lenovo'].json.category_id") }}                                                                                                                                                                
                                                                                                                                                                                                                                            

These JSON formats are fundamental to working with n8n workflows, data transformation, and configuration management.  
