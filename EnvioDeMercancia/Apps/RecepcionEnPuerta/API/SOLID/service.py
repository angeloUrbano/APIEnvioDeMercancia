



from EnvioDeMercancia.Apps.RecepcionEnPuerta.API.SOLID.repositories import RecepcionRepository




class RecepcionService():

    def __init__(self):
        self.repository = RecepcionRepository()

    def serializer_all_boxes(self ,  serializer_class):

        try:
            query = self.repository.get_all_box()
            if query["success"]:
                serializer = serializer_class(query["info"] , many=True)
                return {"success":True , "info":serializer.data}
            return {"success":False , "info":query["info"]}
        
        except Exception as e:
            raise ValueError(str(e))
        

    def serializer_one_boxes(self , pk ,   serializer_class):
        try:
            query = self.repository.get_one_box(pk)
            if query["success"]:
                serializer = serializer_class(query["info"])
                return {"success":True , "info":serializer.data}
            return {"success":False , "info":query["info"]}
        
        except Exception as e:
            raise ValueError(str(e))
        


    def serializer_update_box(self , pk , serializer_class , request):

        try:
            query = self.repository.get_one_box(pk)
            if query["success"]:
                serializer = serializer_class(query["info"] , data=request)

                if serializer.is_valid():
                    serializer.save()
                    return {"success":True , "info":serializer.data}
                return {"success":False , "info":serializer.errors}
                
            return {"success":False , "info":query["info"]}
        
        except Exception as e:
            raise ValueError(str(e))
        



    def serializer_create_box(self , serializer_class , request):

        try:
            serializer = serializer_class(data=request)
            if serializer.is_valid():
                serializer.save()
                return {"success":True , "info":serializer.data}
            return {"success":False , "info":serializer.errors}
                        
        except Exception as e:
            raise ValueError(str(e))
        


    def serializer_delete_box(self , pk , serializer_class):

        try:
            query = self.repository.get_one_box(pk)

            if query["success"]:
                obj = query["info"]
                if obj:
                    obj.is_active =False
                    obj.save()
                    return {"success":True , "info":"elemento eliminado"}
                return {"success":False , "info":"error intentando eliminar el elemento"}
                
            return {"success":False , "info":query["info"]}
        
        except Exception as e:
            raise ValueError(str(e))


        
        

        