tag: user.r
-
run that:key(ctrl-enter)    
go line: key(alt-shift-G)

#ggplot2 commands

plot: 
    'ggplot(aes())'
    key(left)
    key(left) 

aes: insert('aes')

histogram plot: 
    insert('geom_histogram()')
    key( left )

density plot: 
    insert('geom_density()')
    key( left )

column plot: 
    insert('geom_col()')
    key( left ) 

bar plot: 
    insert('geom_bar()')
    key('left')

box plot:
    insert('geom_boxplot()')
    key('left')

line plot:
    insert('geom_line()')
    key('left')

scatter plot:
    insert('geom_point()')
    key('left')


save plot: 
    insert('ggsave()')
    key( left )

line type: 'lty' 

plap: 
    key(end)
    ' +'
    key(enter)

column names: 
    'colnames()'
    key( left )

chain:
    key(end)
    " |>"

chain here:
    " |> "

########## Single cell RNA sequencing ##########

object: 'seurat'
metadata: 'seurat@meta.data'