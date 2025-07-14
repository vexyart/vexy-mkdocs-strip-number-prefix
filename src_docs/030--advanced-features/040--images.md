# Images

## Basic Image Syntax

```markdown
![Alt text](path/to/image.png)
![Alt text](path/to/image.png "Optional title")
```

## Images with Links

```markdown
[![Alt text](image.png)](https://example.com)
```

## Reference-Style Images

```markdown
![Alt text][image-ref]

[image-ref]: path/to/image.png "Optional title"
```

## Image Alignment (with CSS)

<div align="center">

![Centered Image](https://via.placeholder.com/200x100/0088cc/ffffff?text=Centered)

</div>

<div align="right">

![Right Aligned](https://via.placeholder.com/150x75/00aa00/ffffff?text=Right)

</div>

## Images and Prefixes

!!! important "Image Paths"
    Image paths are not affected by the strip-number-prefix plugin. Only markdown files have their URLs transformed.

## Figure Captions

<figure>
  <img src="https://via.placeholder.com/300x200/ff6600/ffffff?text=Figure" alt="Figure example">
  <figcaption>This is a figure caption using HTML</figcaption>
</figure>

[Previous: Admonitions](030--admonitions.md) | [Back to Advanced Features](../030--advanced-features/) | [Next Section: Examples](../040--examples/)