file=$1

sed -i 's/cursor:none/cursor:auto/g' $file/webpack/base.css
sed -i 's/60v/80v/g' $file/webpack/base.css
sed -i 's/ muted/ muted controls/' $file/index.html