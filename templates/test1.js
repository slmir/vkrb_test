varColCntSvern = document.getElementById('columns_count_def').value;
                //for (i=varColCntSvern;i>1;i--){
                    //str1 = "column_select'+i+'"

                    //document.getElementById("column_select'+i+'").disabled = true;
                    //document.getElementById("container'+(i+0)+'").hidden = true;
                //}

                $node = '<div class="input-group mb-3">'
                      + '<span class="column_out_aft_sumbt" id="column_out_aft_sumbt"> Развернуть </span>';

                $(this).parent().after($node);

                document.getElementById("newAddVarCol").remove();
                document.getElementById("column_svern_aft_sumbt").remove();